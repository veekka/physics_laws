from collections import namedtuple
from pytest import approx, fixture, raises
from symplyphysics import (
    errors,
    units,
    Quantity,
    SI,
    convert_to,
)

from symplyphysics.laws.optics import formula_thin_lens_through_curvature as form_len


# There is a lens(refractive index =1.66) on the water(refractive index n2=1.33), (refractive index n2=1.33) n1=1.
# The curvature of the upper side of the lens 6,6cm, the lower 3.3cm. At what distance will the image of the object
# be located if it is located perpendicular to the lens at a height of 10cm? Answer: 0.133cm


@fixture(name="test_args")
def test_args_fixture():
    refractive_index_environment_object = 1
    refractive_index_environment_image = 1.33
    object_distance = Quantity(0.1 * units.meter)
    refractive_index_lens = 1.66
    curvature_first_lens_surface = Quantity(0.066 * units.meter)
    curvature_second_lens_surface = Quantity(0.033 * units.meter)
    Args = namedtuple("Args", ["refractive_index_environment_object", "refractive_index_environment_image",
                               "object_distance", "refractive_index_lens", "curvature_first_lens_surface",
                               "curvature_second_lens_surface"])
    return Args(refractive_index_environment_object=refractive_index_environment_object,
                refractive_index_environment_image=refractive_index_environment_image,
                object_distance=object_distance,
                refractive_index_lens=refractive_index_lens,
                curvature_first_lens_surface=curvature_first_lens_surface,
                curvature_second_lens_surface=curvature_second_lens_surface)


def test_basic_distance(test_args):
    result = form_len.calculate_distance_to_image(test_args.refractive_index_environment_object, test_args.refractive_index_environment_image,
                                                  test_args.object_distance, test_args.refractive_index_lens,
                                                  test_args.curvature_first_lens_surface, test_args.curvature_second_lens_surface)
    assert SI.get_dimension_system().equivalent_dims(result.dimension, units.length)
    result_distance = convert_to(result, units.meter).evalf(4)
    assert result_distance == approx(0.133, 0.01)

