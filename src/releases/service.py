from characteristics.models import CalculatedCharacteristic
from releases.models import Release


def get_planned_values(release: Release):
    planned_values = {}

    for characteristic, value in release.goal.data.items():
        planned_values[characteristic] = value / 100

    return planned_values


def get_accomplished_values(release: Release, repositories_ids: list[int]):
    result_calculated = CalculatedCharacteristic.objects.filter(release=release).all()

    if len(result_calculated) == 0:
        result_calculated = (
            get_calculated_characteristic_by_ids_repositories(
                repositories_ids
            )
        )

    return get_process_calculated_characteristics(list(result_calculated))


def get_process_calculated_characteristics(
    result_calculated: list[CalculatedCharacteristic],
):
    accomplished = {}
    for calculated_characteristic in result_calculated:
        characteristic = calculated_characteristic.characteristic.key
        repository = calculated_characteristic.repository.name

        if repository not in accomplished:
            accomplished[repository] = {}
        accomplished[repository].update(
            {characteristic: calculated_characteristic.value}
        )
    return accomplished


def get_calculated_characteristic_by_ids_repositories(
    ids_repositories: list[int],
):
    result_calculated = []
    for id_repository in ids_repositories:
        calculated_characteristic = (
            CalculatedCharacteristic.objects.filter(
                repository_id=id_repository, release=None
            )
            .all()
            .order_by('-created_at')[:2]
        )
        result_calculated = result_calculated + list(calculated_characteristic)
    return result_calculated


def get_arrays_diff(goal_data: dict, characteristic_repo: dict):
    array_rp = []
    array_rd = []

    for characteristic in 'reliability', 'maintainability':
        try:
            if (
                goal_data[characteristic]
                and characteristic_repo[characteristic]
            ):
                array_rp.append(goal_data[characteristic] / 100)
                array_rd.append(characteristic_repo[characteristic])
        except Exception:
            continue

    return array_rp, array_rd
