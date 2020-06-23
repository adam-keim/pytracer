from raytracer.base import Canvas, Color


def test_canvas():
    c = Canvas(10, 20)
    assert c.width == 10
    assert c.height == 20
    for row in c.pixels:
        for pixel in row:
            assert pixel == Color(0, 0, 0)


def test_write_canvas():
    c = Canvas(10, 20)
    red = Color(1, 0, 0)
    c.write_pixel(2, 3, red)
    assert c.read_pixel(2, 3) == red


def test_header():
    c = Canvas(5, 3)
    assert c.to_ppm().startswith("P3\n5 3\n255\n")


def test_ppm():
    c = Canvas(5, 3)
    c1 = Color(1.5, 0, 0)
    c2 = Color(0, 0.5, 0)
    c3 = Color(-0.5, 0, 1)
    c.write_pixel(0, 0, c1)
    c.write_pixel(2, 1, c2)
    c.write_pixel(4, 2, c3)
    assert (
        "255 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 128 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 255"
        in c.to_ppm()
    )


def test_long_ppm():
    c = Canvas(10, 2, Color(1.0, 0.8, 0.6))
    assert (
        "255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204\n153 255 204 153 255 204 153 255 204 153 255 204 153\n255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204\n153 255 204 153 255 204 153 255 204 153 255 204 153"
        in c.to_ppm()
    )


def test_newline():
    c = Canvas(5, 3)
    assert c.to_ppm().endswith("\n")
