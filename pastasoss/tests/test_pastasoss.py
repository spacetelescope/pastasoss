from pastasoss.soss_traces import rotate 

def test_rotate():

    x = [1, 2, 3, 4]
    y = [5, 6, 7, 8]

    x_coords, y_coords = rotate(x, y, 45.)
    print(x_coords, y_coords)

    assert all([coord_1 == coord_2 for coord_1, coord_2 in zip(x_coords, x)])
