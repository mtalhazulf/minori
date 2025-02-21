<template>
  <q-dialog v-model="internalDialog">
    <q-card>
      <q-card-section>
        <q-input v-model="label" label="Nome" outlined class="q-my-sm" />
        <q-input
          v-model="description"
          label="Descrizione"
          outlined
          class="q-my-sm" />
      </q-card-section>
      <q-card-actions align="right">
        <q-btn
          v-close-popup
          label="Annulla"
          flat
          color="primary"
          @click="close()" />
        <q-btn
          :label="isEdit ? 'Modifica' : 'Crea'"
          color="primary"
          @click="emitsNewTaskTypeModule()" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
export default {
  name: 'DialogNewTaskTypeModule',
  props: {
    dialog: {
      type: Boolean,
      required: true
    },
    parentId: {
      type: String,
      required: true
    },
    idProp: {
      type: String,
      required: false,
      default: ''
    },
    labelProp: {
      type: String,
      required: false,
      default: ''
    },
    descriptionProp: {
      type: String,
      required: false,
      default: ''
    }
  },
  emits: ['update:dialog', 'newTaskTypeModule', 'editTaskTypeModule'],
  data() {
    return {
      label: '',
      description: '',
      internalDialog: false,
      isEdit: false
    }
  },
  watch: {
    dialog(val) {
      if (this.labelProp !== '') {
        this.isEdit = true
        this.label = this.labelProp
        this.description = this.descriptionProp
      } else {
        this.isEdit = false
        this.label = ''
        this.description = ''
      }
      this.internalDialog = val
    },
    internalDialog(val) {
      this.$emit('update:dialog', val)
    }
  },
  methods: {
    close() {
      this.internalDialog = false
    },
    emitsNewTaskTypeModule() {
      if (!this.label) {
        this.$q.notify({
          message: 'Il nome è obbligatorio',
          color: 'warning',
          icon: 'report_problem',
          position: 'top-right'
        })
        return
      }
      if (
        this.isEdit &&
        this.label === this.labelProp &&
        this.description === this.descriptionProp
      ) {
        this.$q.notify({
          message: 'Nessuna modifica effettuata',
          color: 'warning',
          icon: 'report_problem',
          position: 'top-right'
        })
        return
      }
      this.$emit('newTaskTypeModule', {
        label: this.label,
        description: this.description,
        parentId: this.parentId,
        id: this.idProp,
        isEdit: this.isEdit
      })
      this.internalDialog = false
    }
  }
}
</script>
