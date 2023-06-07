#!/usr/bin/env python3
import pygame, math

def draw_pixel(surface: pygame.Surface, pos: tuple[int, int], color:tuple[int, int, int]):
    surface.set_at(pos, color)

def flatten_3d(pos: tuple[int, int, int], focal_length) -> tuple[int, int]|None:
    if pos[2] <= 0-focal_length:
        return None
    try:
        return (((pos[0] * focal_length)//(pos[2] + focal_length)), ((pos[1] * focal_length)//(pos[2] + focal_length)))
    except ZeroDivisionError:
        return None

def center_origin(surf, p):
    return (p[0] + surf.get_width() // 2, p[1] + surf.get_height() // 2)

def gen_cube(mid_pos: tuple[int, int, int], size: int):
    half = size//2
    vertices_3d = (
        #front face
        (mid_pos[0]-half, mid_pos[1]-half, mid_pos[2]-half),
        (mid_pos[0]-half, mid_pos[1]+half, mid_pos[2]-half),
        (mid_pos[0]+half, mid_pos[1]+half, mid_pos[2]-half),
        (mid_pos[0]+half, mid_pos[1]-half, mid_pos[2]-half),
        #back face
        (mid_pos[0]-half, mid_pos[1]-half, mid_pos[2]+half),
        (mid_pos[0]-half, mid_pos[1]+half, mid_pos[2]+half),
        (mid_pos[0]+half, mid_pos[1]+half, mid_pos[2]+half),
        (mid_pos[0]+half, mid_pos[1]-half, mid_pos[2]+half),
    )

    return vertices_3d


def rotate_vertex_y(pos: tuple[int, int, int], center: tuple[int, int, int], theta):
    #rotation
    # [x, y, z] * [cos  0 sin]  =  [xr, yr, zr]
    #             [0    1   0]
    #             [-sin 0 cos]

    xt, y, zt = pos[0]-center[0], pos[1], pos[2]-center[2]
    x_rotated = xt*math.cos(theta) - zt*math.sin(theta)
    y_rotated = y
    z_rotated = xt*math.sin(theta) + zt*math.cos(theta)

    return (int(x_rotated + center[0]), int(y_rotated), int(z_rotated + center[2]))

def main():
    size = (900, 600)
    focal_length = 250

    theta = 0

    pygame.init()
    window: pygame.Surface = pygame.display.set_mode((size[0], size[1]))
    pygame.display.set_caption('Basic Pygame Template')

    color = {"white": (255, 255, 255), "red": (255, 0, 0), "black": (0, 0, 0)}

    cube_center = (0, 10, 50)
    vertices = gen_cube(cube_center, 100)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    cube_center = (cube_center[0], cube_center[1], cube_center[2]-10)
                if event.y == -1:
                    cube_center = (cube_center[0], cube_center[1], cube_center[2]+10)
        if not run:
            break

        window.fill(color["black"])

        cube_center = (cube_center[0], int(25*math.sin(theta*2)), cube_center[2])

        vertices = gen_cube(cube_center, 100)
        vertices_rotated = [rotate_vertex_y(i, cube_center, theta) for i in vertices]
        flattened = [flatten_3d(i, focal_length) for i in vertices_rotated]

        edges = {
            flattened[0]: (flattened[1], flattened[3], flattened[4]),
            flattened[1]: (flattened[2], flattened[5]),
            flattened[2]: (flattened[3], flattened[6]),
            flattened[3]: (flattened[7],),

            flattened[4]: (flattened[5], flattened[7]),
            flattened[5]: (flattened[6],),
            flattened[6]: (flattened[7],),
            # flattened[7] no need, as its alr connected to 3 other nodes
        }

        #window.set_at(mid_point, color["red"])
        for vertex in flattened:
            if vertex is not None:
                window.set_at(center_origin(window, vertex), color["white"])
        for key, val in edges.items():
            if key is not None:
                for vertex in val:
                    if vertex is not None:
                        pygame.draw.line(window, color["white"], center_origin(window, key), center_origin(window, vertex))

        theta += 0.001

        pygame.display.flip()

if __name__ == "__main__":
    main()