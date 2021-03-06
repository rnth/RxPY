from rx.core import ObservableBase


def buffer(source, buffer_openings=None, buffer_closing_mapper=None) -> ObservableBase:
    """Projects each element of an observable sequence into zero or more
    buffers.

    Keyword arguments:
    buffer_openings -- Observable sequence whose elements denote the
        creation of windows.
    buffer_closing_mapper -- [optional] A function invoked to define
        the closing of each produced window. If a closing mapper
        function is specified for the first parameter, this parameter is
        ignored.

    Returns an observable sequence of windows.
    """

    return source.window(buffer_openings, buffer_closing_mapper).flat_map(lambda item: item.to_iterable().map(list))


def buffer_with_count(source, count, skip=None) -> ObservableBase:
    """Projects each element of an observable sequence into zero or more
    buffers which are produced based on element count information.

    Example:
    res = xs.buffer_with_count(10)
    res = xs.buffer_with_count(10, 1)

    Keyword parameters:
    count -- {Number} Length of each buffer.
    skip -- {Number} [Optional] Number of elements to skip between
        creation of consecutive buffers. If not provided, defaults to
        the count.

    Returns an observable {Observable} sequence of buffers.
    """

    if skip is None:
        skip = count

    def mapper(value):
        return value.to_iterable().map(list)

    def predicate(value):
        return len(value) > 0

    return source.window_with_count(count, skip).flat_map(mapper).filter(predicate)
