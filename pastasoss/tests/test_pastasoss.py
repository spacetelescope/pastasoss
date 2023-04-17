from pastasoss.soss_traces import rotate 

def test_rotate():

    x = [1, 2, 3, 4]
    y = [5, 6, 7, 8]

    x_coords, y_coords = rotate(x, y, 45.)

    assert x_coords == x 
