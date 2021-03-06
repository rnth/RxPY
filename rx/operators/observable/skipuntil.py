from rx.core import Observable, ObservableBase, AnonymousObservable
from rx.disposables import CompositeDisposable, SingleAssignmentDisposable
from rx.internal.utils import is_future


def skip_until(source, other: ObservableBase) -> ObservableBase:
    """Returns the values from the source observable sequence only after
    the other observable sequence produces a value.

    other -- The observable sequence that triggers propagation of
        elements of the source sequence.

    Returns an observable sequence containing the elements of the source
    sequence starting from the point the other sequence triggered
    propagation.
    """

    other = Observable.from_future(other) if is_future(other) else other

    def subscribe(observer, scheduler=None):
        is_open = [False]

        def on_next(left):
            if is_open[0]:
                observer.on_next(left)

        def on_completed():
            if is_open[0]:
                observer.on_completed()

        subs = source.subscribe_(on_next, observer.on_error, on_completed, scheduler)
        disposables = CompositeDisposable(subs)

        right_subscription = SingleAssignmentDisposable()
        disposables.add(right_subscription)

        def on_next2(x):
            is_open[0] = True
            right_subscription.dispose()

        def on_completed2():
            right_subscription.dispose()

        right_subscription.disposable = other.subscribe_(on_next2, observer.on_error, on_completed2, scheduler)

        return disposables
    return AnonymousObservable(subscribe)
