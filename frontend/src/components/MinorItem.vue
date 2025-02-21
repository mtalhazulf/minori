<template>
  <q-item class="minor-box q-pa-xs-xs" draggable="true">
    <q-item-section> {{ minor.name }} {{ minor.surname }} </q-item-section>
    <q-item-section v-if="fastRemove" avatar>
      <q-btn
        flat
        round
        dense
        icon="close"
        color="negative"
        @click="$emit('remove')" />
    </q-item-section>
  </q-item>
</template>

<script>
export default {
  name: 'MinorCard',
  props: {
    minor: {
      type: Object,
      required: true
    },
    fastRemove: {
      type: Boolean,
      default: false
    }
  },
  emits: ['remove']
}
</script>
