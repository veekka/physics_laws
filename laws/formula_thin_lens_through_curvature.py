from sympy import (Eq, solve)
from symplyphysics import (units, Quantity, dimensionless, Symbol, print_expression, validate_input,
   validate_output)

import math

# Law: n2 / a2 + n1 / a1 = (n - n1) / R1 +  (n - n2) / R2
# Where:
# R1/R2 - radius of curvature of the first/second lens surfaces
# n1/n2 - the refractive index of the environment in which the object/image are located
# a1 - the distance from the object to the center of the lens
# a2 - the distance from the center of the lens to the image
# n - refractive index of the lens
# ! for thin lens: lens thickness << radius of curvature of the bounding surfaces


refractive_index_environment_object = Symbol("refractive_index_environment_object", dimensionless) # n1
refractive_index_environment_image = Symbol("refractive_index_environment_image", dimensionless) # n2
distance_to_object = Symbol("distance_to_object", units.length)  # a1
distance_to_image = Symbol("distance_to_image", units.length) # a2
refractive_index_lens = Symbol("refractive_index_lens", dimensionless) # n
curvature_first_lens_surface = Symbol("curvature_first_lens_surface", units.length)# R1
curvature_second_lens_surface = Symbol("curvature_second_lens_surface", units.length) # R2

first_term = refractive_index_environment_image / distance_to_image
second_term = refractive_index_environment_object / distance_to_object
third_term = (refractive_index_lens - refractive_index_environment_object) / curvature_first_lens_surface
fourth_term = (refractive_index_lens - refractive_index_environment_image) / curvature_second_lens_surface

if curvature_first_lens_surface == 0:
    third_term = 0
elif curvature_second_lens_surface == 0:
    fourth_term = 0

law = Eq(first_term + second_term, third_term + fourth_term)

# law = Eq((refractive_index_environment_image / distance_to_image) + (refractive_index_environment_object / distance_to_object),
#          ((refractive_index_lens - refractive_index_environment_object) / curvature_first_lens_surface) +
#          ((refractive_index_lens - refractive_index_environment_image) / curvature_second_lens_surface))


def print_law() -> str:
    return print_expression(law)


@validate_input(refractive_index_environment_object_=refractive_index_environment_object,
                refractive_index_environment_image_=refractive_index_environment_image,
                object_distance_=distance_to_object,
                refractive_index_lens_=refractive_index_lens,
                curvature_first_lens_surface_=curvature_first_lens_surface,
                curvature_second_lens_surface_=curvature_second_lens_surface)
@validate_output(distance_to_image)
def calculate_distance_to_image(refractive_index_environment_object_: Quantity | float, refractive_index_environment_image_: Quantity | float,
                    object_distance_: Quantity | float, refractive_index_lens_: Quantity | float, curvature_first_lens_surface_: Quantity | float,
                    curvature_second_lens_surface_: Quantity | float) -> Quantity:

    result_expr = solve(law, distance_to_image, dict=True)[0][distance_to_image]
    res_distance = result_expr.subs({
        refractive_index_environment_object: refractive_index_environment_object_,
        refractive_index_environment_image: refractive_index_environment_image_,
        distance_to_object: object_distance_,
        refractive_index_lens: refractive_index_lens_,
        curvature_first_lens_surface: curvature_first_lens_surface_,
        curvature_second_lens_surface: curvature_second_lens_surface_
    })
    return Quantity(res_distance)