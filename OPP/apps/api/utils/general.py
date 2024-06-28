import typing


def get_data_by_page(data: list[typing.Any], page_id: int, page_size: int) -> list[typing.Any]:
    start_index = (page_id - 1) * page_size
    stop_index = page_id * page_size
    result = data[start_index:stop_index]
    return result

