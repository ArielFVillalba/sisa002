from crum import get_current_user
from django.contrib.postgres import serializers
from django.core.serializers import json, serialize
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
import json

from django.forms import model_to_dict


@receiver(pre_save)
def pre_save(sender, instance, **kwargs):

    user = get_current_user()
    if not user or (user.is_authenticated):
        try:
            old_instance = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            old_instance = None

        if old_instance:
            old_instance = sender.objects.get(pk=instance.pk)
            print("pre save actualiso "+ str(old_instance))
        else:

            action = 'create'
            print("pre save creo "+ str(old_instance)+action)

    else:
        pass


@receiver(pre_delete)
def pre_delete(sender, instance, **kwargs):
    user = get_current_user()

    if not user or (user.is_authenticated):
        print("pre eliminar {instance}")

        instance.user = user
        instance.save()


@receiver(post_save)
def post_save(sender, instance, created, **kwargs):
    # Código que se ejecutará después de guardar o modificar el objeto TuModelo
    # 'created' es True si el objeto se acaba de crear, False si se actualizó.}
    user = get_current_user()  # Asegúrate de que esta función esté correctamente implementada
    if not user or (user.is_authenticated):
        if created:
            old_instance = sender.objects.get(pk=instance.pk)

            print("post save  create Se creó un nuevo registro {instance}")

        else:
            print("post Seve updaete actualizó un  registro {instance}")

    else:
            pass


@receiver(post_delete)
def post_delete(sender, instance, **kwargs):
    print("post eliminar")
    # Código que se ejecutará después de eliminar el objeto TuModelo
    # print(f"Objeto {instance} fue eliminado.")
