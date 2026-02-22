class BaseService:
    model = None

    def get_model(self):
        if self.model is None:
            raise NotImplementedError("model must be set in Meta class")
        return self.model

    def get_queryset(self):
        return self.get_model().objects.all()

    def create(self, validated_data: dict):
        return self.get_model().objects.create(**validated_data)

    def update(self, instance, validated_data: dict):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def soft_delete(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance

    class Meta:
        model = None
