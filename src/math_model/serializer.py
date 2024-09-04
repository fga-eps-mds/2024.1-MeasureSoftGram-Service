from rest_framework import serializers

from characteristics.models import SupportedCharacteristic
from characteristics.serializers import SupportedCharacteristicSerializer
from measures.serializers import SupportedMeasureSerializer
from release_configuration.models import ReleaseConfiguration
from subcharacteristics.serializers import SupportedSubCharacteristicSerializer


class GithubJSONSerializer(serializers.Serializer): 
    metrics = serializers.DictField()


class SonarQubeJSONSerializer(serializers.Serializer):
    """
    Serializer for SonarQube JSON data.
    """

    paging = serializers.DictField()
    baseComponent = serializers.DictField()
    components = serializers.ListField()


class MetricsSerializer(serializers.Serializer):
    product_id: serializers.IntegerField()
    repository_id: serializers.IntegerField()
    organization_id: serializers.IntegerField()
    sonarqube: SonarQubeJSONSerializer()
    github: serializers.DictField()
    

