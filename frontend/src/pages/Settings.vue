<template>
  <q-page class="q-mx-xl">
    <div class="row">
      <Heading :title="'Impostazioni'" />
    </div>
    <div class="row">
      <div class="q-gutter-y-md" style="width: 100%">
        <q-tabs
          v-model="tab"
          indicator-color="green"
          class="text-teal"
          inline-label>
          <q-tab
            v-if="operator === 'superadmin'"
            name="badge"
            icon="alarm"
            label="Badge" />
          <q-tab
            v-if="operator === 'superadmin'"
            name="roles"
            icon="person"
            label="Ruoli"
            @click="getRoles()" />
          <q-tab
            name="tasks"
            icon="assignment"
            label="Mansioni"
            @click="getSettingsTasks()" />
          <q-tab
            v-if="operator === 'superadmin'"
            name="iva"
            icon="euro_symbol"
            label="IVA"
            @click="getIVA()" />
        </q-tabs>

        <q-tab-panels v-model="tab" animated>
          <q-tab-panel v-if="operator === 'superadmin'" name="badge">
            <div class="text-h6">Assegna Badge</div>
            <div>
              <div v-for="(badge, index) in badges" :key="index" class="row">
                <div class="col-4">
                  <q-select
                    v-model="badge.operator"
                    label="Operatore"
                    :options="operators.length === 0 ? [] : operators"
                    :option-label="opt => opt.name + ' ' + opt.surname"
                    emit-value
                    @update:model-value="check($event, index)"
                    ><template #no-option>
                      <q-item>
                        <q-item-section class="text-italic text-grey">
                          Nessun operatore disponibile
                        </q-item-section>
                      </q-item>
                    </template></q-select
                  >
                </div>
                <div class="col-4 q-ml-md">
                  <q-input
                    v-model="badge.badgeId"
                    label="N. Badge"
                    type="text"
                    placeholder="0000000x"
                    maxlength="9"
                    @change="formatBadge($event, badge)" />
                </div>

                <div class="col-2">
                  <div class="block float-right">
                    <q-btn
                      v-if="badges.length !== 1"
                      round
                      icon="delete"
                      color="red"
                      @click="
                        askConfirm(
                          `Sei sicuro di voler dissociare l'operatore dal badge?`,
                          removeBadge,
                          index
                        )
                      " />
                    <q-btn
                      v-if="badges.length === 1"
                      round
                      icon="delete"
                      color="red"
                      @click="
                        () => {
                          badge.operator = null
                          badge.badgeId = null
                        }
                      " />
                    <q-btn
                      v-if="index + 1 === badges.length"
                      round
                      icon="add"
                      color="green"
                      class="q-ml-sm"
                      @click="addBadge" />
                  </div>
                </div>
              </div>
              <div class="row q-mt-lg">
                <q-btn
                  label="Salva modifiche"
                  color="green"
                  @click="
                    askConfirm(
                      'Sei sicuro di voler salvare le modifiche?',
                      save
                    )
                  " />
              </div>
            </div>
          </q-tab-panel>

          <q-tab-panel v-if="operator === 'superadmin'" name="roles">
            <div class="text-h6">Ruoli operatore</div>
            <div class="row q-my-md">
              <q-table
                v-model:pagination="pagination"
                :rows="roles"
                :columns="columns"
                row-key="_id"
                :loading="data_loading"
                :rows-per-page-options="[5, 8, 10, 15, 25, 50]"
                style="width: 100%">
                <template #top-right>
                  <q-btn
                    color="secondary"
                    label="Aggiungi ruolo"
                    style="width: 180px"
                    class="q-mr-md"
                    @click="
                      () => {
                        reset()
                        isEdit = false
                        dialog = true
                      }
                    " />
                  <q-dialog v-model="dialog">
                    <q-card>
                      <q-card-section>
                        <div class="text-h6">Nuovo ruolo</div>
                      </q-card-section>

                      <q-card-section class="q-pt-none">
                        <form class="q-my-sm">
                          <q-input
                            v-model="role.name"
                            outlined
                            label="Livello"
                            class="q-my-sm" />
                          <q-input
                            v-model="role.label"
                            outlined
                            label="Ruolo"
                            class="q-my-sm" />
                          <q-input
                            v-model="role.description"
                            outlined
                            label="Descrizione"
                            class="q-my-sm" />
                          <q-input
                            v-model="role.average_hour_cost"
                            outlined
                            label="Importo"
                            type="number"
                            prefix="€"
                            class="q-my-sm" />
                        </form>
                      </q-card-section>

                      <q-card-actions align="right">
                        <q-btn
                          v-close-popup
                          flat
                          label="Cancella"
                          color="primary"
                          @click="reset()" />
                        <q-btn
                          :label="isEdit ? 'Salva' : 'Aggiungi'"
                          color="primary"
                          :disable="!validateRole()"
                          @click="isEdit ? editRole() : addRole()" />
                      </q-card-actions>
                    </q-card>
                  </q-dialog>
                </template>
                <template #body-cell-actions="props">
                  <q-td
                    style="
                      display: flex;
                      justify-content: center;
                      align-items: center;
                    ">
                    <q-btn
                      round
                      icon="edit"
                      color="green"
                      size="sm"
                      class="q-ml-lg"
                      @click="edit(props.row)" />
                    <q-btn
                      round
                      icon="delete"
                      color="red"
                      size="sm"
                      class="q-ml-lg"
                      @click="
                        askConfirm(
                          'Sei sicuro di voler eliminare il ruolo?',
                          deleteRole,
                          props.row
                        )
                      "
                  /></q-td>
                </template>
                <template #no-data="{ message }">
                  <div
                    class="full-width row flex-center text-primary q-gutter-sm">
                    <div v-if="message === 'Loading...'">{{ message }}</div>
                    <div v-else>
                      <q-icon size="2em" name="sentiment_dissatisfied" />
                      <span>
                        {{
                          errDataMsg
                            ? 'Impossibile caricare i ruoli al momento..'
                            : 'Nessun ruolo presente ...'
                        }}
                      </span>
                    </div>
                  </div>
                </template>
              </q-table>
            </div>
          </q-tab-panel>

          <q-tab-panel name="tasks">
            <div class="text-h6">Modifica mansioni</div>
            <q-list
              bordered
              separator
              class="rounded-borders"
              style="max-width: 50%">
              <q-expansion-item
                v-for="taskT in settingsTasks"
                :key="taskT._id"
                expand-icon-toggle
                expand-separator
                :content-inset-level="1"
                :label="taskT.label">
                <template #header>
                  <q-item-section side>
                    <q-btn
                      round
                      icon="delete"
                      color="red"
                      @click="
                        askConfirm(
                          'Sei sicuro di voler rimuovere la tipologia di mansione?',
                          removeTaskType,
                          taskT._id
                        )
                      " />
                  </q-item-section>
                  <q-item-section avatar>
                    <q-btn
                      round
                      icon="edit"
                      color="yellow"
                      @click="
                        () => {
                          taskLabelToEdit = taskT.label
                          taskDescriptionToEdit = taskT.description
                          id = taskT._id
                          dialogNewTaskTypeModule = true
                        }
                      " />
                  </q-item-section>
                  <q-item-section>
                    <q-item-label>
                      {{ taskT.label }}
                    </q-item-label>
                    <q-item-label caption>
                      {{ taskT.description }}
                    </q-item-label>
                  </q-item-section>
                </template>
                <q-list separator>
                  <q-item v-for="taskM in taskT.modules" :key="taskM._id">
                    <q-item-section avatar>
                      <q-btn
                        round
                        icon="delete"
                        color="red"
                        @click="
                          askConfirm(
                            'Sei sicuro di voler rimuovere il modulo?',
                            removeTaskModule,
                            taskM._id,
                            taskT._id
                          )
                        " />
                    </q-item-section>
                    <q-item-section avatar>
                      <q-btn
                        round
                        icon="edit"
                        color="yellow"
                        @click="
                          () => {
                            taskLabelToEdit = taskM.label
                            taskDescriptionToEdit = taskM.description
                            id = taskM._id
                            parentId = taskT._id
                            dialogNewTaskTypeModule = true
                          }
                        " />
                    </q-item-section>
                    <q-item-section>
                      <q-item-label>
                        {{ taskM.label }}
                      </q-item-label>
                      <q-item-label caption>
                        {{ taskM.description }}
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section avatar>
                      <q-btn
                        round
                        icon="add"
                        color="green"
                        @click="
                          () => {
                            parentId = taskT._id
                            dialogNewTaskTypeModule = true
                          }
                        " />
                    </q-item-section>
                    <q-item-section> Aggiungi modulo </q-item-section>
                  </q-item>
                </q-list>
              </q-expansion-item>
              <q-item bordered>
                <q-item-section avatar>
                  <q-btn
                    round
                    icon="add"
                    color="green"
                    @click="
                      () => {
                        dialogNewTaskTypeModule = true
                      }
                    " />
                </q-item-section>
                <q-item-section> Aggiungi tipologia </q-item-section>
              </q-item>
            </q-list>
            <DialogNewTaskTypeModule
              v-model:dialog="dialogNewTaskTypeModule"
              :parent-id="parentId"
              :description-prop="taskDescriptionToEdit"
              :label-prop="taskLabelToEdit"
              :id-prop="id"
              @new-task-type-module="
                val => {
                  taskLabelToEdit = ''
                  taskDescriptionToEdit = ''
                  if (val.parentId !== '') {
                    if (val.isEdit) {
                      editTaskModule(
                        val.label,
                        val.description,
                        val.id,
                        val.parentId
                      )
                    } else {
                      addTaskModule(val.label, val.description, val.parentId)
                    }
                  } else {
                    if (val.isEdit) {
                      editTaskType(val.label, val.description, val.id)
                    } else {
                      addTaskType(val.label, val.description)
                    }
                  }
                }
              " />
          </q-tab-panel>
          <q-tab-panel name="iva"
            ><div class="text-h6">Modifica IVA</div>
            <q-item style="max-width: 300px">
              <q-item>
                <q-item-section>
                  <q-item-label overline>IVA</q-item-label>
                  <q-input
                    v-model="iva"
                    type="number"
                    min="0"
                    max="100"
                    dense
                    bordered
                    suffix="%" />
                </q-item-section>
                <q-item-section side>
                  <q-btn round icon="save" color="green" @click="saveIVA()" />
                </q-item-section>
              </q-item>
            </q-item>
          </q-tab-panel>
        </q-tab-panels>
      </div>
    </div>
  </q-page>
</template>

<script>
import Heading from 'components/Heading.vue'
import { useQuasar } from 'quasar'
import { api } from 'src/boot/axios'
import DialogNewTaskTypeModule from 'src/components/DialogNewTaskTypeModule.vue'

export default {
  name: 'Settings',
  components: {
    Heading,
    DialogNewTaskTypeModule
  },
  setup() {
    const $q = useQuasar()

    return {
      showNotif(tp, msg) {
        $q.notify({
          type: tp,
          message: msg,
          position: 'top-right',
          timeout: 1500
        })
      }
    }
  },
  data() {
    return {
      tab: 'badge',
      badges: [],
      blockRemoval: true,
      operators: [],
      allOperators: [],
      initOperators: [],
      cannotSave: false,
      operator: '',
      roles: [],
      settingsTasks: [],
      iva: 0,
      columns: [
        {
          name: 'name',
          align: 'center',
          label: 'Livello',
          field: 'name',
          sortable: true
        },
        {
          name: 'label',
          align: 'center',
          label: 'Ruolo',
          field: 'label',
          sortable: true
        },
        {
          name: 'description',
          align: 'center',
          label: 'Descrizione',
          field: 'description',
          sortable: true
        },
        {
          name: 'average_hour_cost',
          align: 'center',
          label: 'Importo ',
          field: 'average_hour_cost',
          sortable: true
        },
        {
          name: 'actions',
          align: 'center',
          label: 'Azioni',
          sortable: true
        }
      ],
      data_loading: true,
      errDataMsg: false,
      pagination: {
        page: 0,
        rowsPerPage: 8
      },
      isEdit: false,
      dialog: false,
      dialogNewTaskTypeModule: false,
      parentId: '',
      id: '',
      taskLabelToEdit: '',
      taskDescriptionToEdit: '',
      role: {
        name: '',
        label: '',
        description: '',
        average_hour_cost: null
      }
    }
  },
  watch: {
    dialogNewTaskTypeModule(val) {
      if (!val) {
        this.taskLabelToEdit = ''
        this.taskDescriptionToEdit = ''
        this.id = ''
        this.parentId = ''
      }
    }
  },
  mounted() {
    this.operator = JSON.parse(sessionStorage.getItem('user')).usertype
    this.tab = this.operator === 'superadmin' ? 'badge' : 'tasks'
    this.tab === 'tasks' && this.getSettingsTasks()
    this.operator === 'superadmin' && this.getOperators()
    this.addBadge()
  },
  methods: {
    editTaskModule(label, description, id, parentId) {
      api
        .patch(`/settings/setting/task/${parentId}/${id}`, {
          label,
          name: label,
          description
        })
        .then(() => {
          this.showNotif('positive', 'Modulo modificato con successo')
          this.getSettingsTasks()
        })
        .catch(() => {
          this.showNotif('negative', 'Errore nella modifica del modulo')
        })
    },
    editTaskType(label, description, id) {
      api
        .patch(`/settings/setting/task/${id}`, {
          label,
          name: label,
          description
        })
        .then(() => {
          this.showNotif('positive', 'Tipologia modificata con successo')
          this.getSettingsTasks()
        })
        .catch(() => {
          this.showNotif('negative', 'Errore nella modifica della tipologia')
        })
    },
    addTaskType(label, description) {
      // TODO vedere se il nome va modificato
      api
        .post('/settings/setting/task', {
          label,
          name: label,
          description
        })
        .then(() => {
          this.showNotif('positive', 'Tipologia creata con successo')
          this.getSettingsTasks()
        })
        .catch(() => {
          this.showNotif('negative', 'Errore nella creazione della tipologia')
        })
    },
    removeTaskType(id) {
      api
        .delete(`/settings/setting/task/${id}`)
        .then(() => {
          this.showNotif('positive', 'Tipologia rimossa con successo')
          this.getSettingsTasks()
        })
        .catch(() => {
          this.showNotif('negative', 'Errore nella rimozione della tipologia')
        })
    },
    addTaskModule(label, description, parentId) {
      // TODO vedere se il nome va modificato
      api
        .post(`/settings/setting/task/${parentId}`, {
          label,
          name: label,
          description
        })
        .then(() => {
          this.showNotif('positive', 'Modulo creato con successo')
          this.getSettingsTasks()
        })
        .catch(e => {
          this.showNotif('negative', 'Errore nella creazione del modulo')
        })
    },
    removeTaskModule(taskModuleId, taskTypeParentId) {
      api
        .delete(`/settings/setting/task/${taskTypeParentId}/${taskModuleId}`)
        .then(() => {
          this.showNotif('positive', 'Modulo rimosso con successo')
          this.getSettingsTasks()
        })
        .catch(e => {
          this.showNotif('negative', 'Errore nella rimozione del modulo')
        })
    },
    getSettingsTasks() {
      api
        .get('/settings/setting/task')
        .then(response => {
          this.settingsTasks = response.data
        })
        .catch(er => {})
    },
    getIVA() {
      api
        .get('/settings/setting/iva')
        .then(response => {
          this.iva = response.data.value
        })
        .catch(er => {})
    },
    saveIVA() {
      api
        .post('/settings/setting/iva', {
          value: parseInt(this.iva),
          timestamp: new Date()
        })
        .then(() => {
          this.showNotif('positive', 'IVA modificata con successo')
        })
        .catch(() => {
          this.showNotif('negative', "Errore nella modifica dell'IVA")
        })
    },
    addBadge() {
      const checkEmptyBadges = this.badges.filter(
        badge => badge.badgeId === null
      )

      if (checkEmptyBadges.length >= 1 && this.badges.length > 0) {
        return
      }
      this.badges.push({
        badgeId: null,
        operator: null
      })
      this.blockRemoval = this.badges.length <= 1
    },

    removeBadge(number) {
      this.blockRemoval = this.badges.length <= 1
      if (!this.blockRemoval) {
        this.badges.splice(number, 1)
      }
    },
    getOperators() {
      api.get('/auth/user/operators').then(r => {
        const response = r.data.filter(el => {
          if (el.status === 'enabled' || !el?.status) {
            return el
          }
        })
        this.initOperators = response
        this.operators = response
        this.allOperators = response.filter(e => {
          if (e?.badgeId) {
            return e
          }
        })
        this.allOperators = this.allOperators.map(x => {
          return { badgeId: x.badgeId, operator: x }
        })
        const opBadges = response.filter(e => {
          if (e?.badgeId) {
            return e
          }
        })
        if (response.length > 0 && opBadges.length > 0) {
          this.badges = response.filter(e => {
            if (e?.badgeId) {
              return e
            }
          })
          this.badges = this.badges.map(x => {
            return { badgeId: x.badgeId, operator: x }
          })
        }
      })
    },
    formatBadge(e, badge) {
      if (Number.isNaN(parseInt(e))) {
        badge.badgeId = null
        this.showNotif('warning', 'Il badge non può contenere lettere')
      } else if (parseInt(e) !== 0 && e !== '') {
        const badgesList = this.badges.filter(el => {
          if (el !== badge) {
            return el
          }
        })
        if (e.length < 9) {
          while (e.length < 9) e = '0' + e
        }
        if (!badgesList.find(el => el.badgeId === e)) {
          badge.badgeId = e
          this.cannotSave = false
        } else {
          badge.badgeId = null
          if (badgesList.find(el => el.badgeId === e)) {
            this.showNotif(
              'warning',
              'Il badge inserito appartiene già ad un operatore. Si prega di inserirne un altro'
            )
            this.cannotSave = true
          }
        }
      } else {
        badge.badgeId = null
      }
    },

    checkRemovedBadges(result, res) {
      this.allOperators.forEach(el => {
        if (result.find(x => x.operator === el.operator) === undefined) {
          res.push({
            badgeId: null,
            operator: el.operator._id.$oid
          })
        }
      })
    },
    validate() {
      let isValid = true
      this.badges.forEach(e => {
        if (
          (e.badgeId === null && e.operator !== null) ||
          (e.badgeId !== null && e.operator === null)
        ) {
          if (e.badgeId === null) {
            this.showNotif('warning', 'Il badge è obbligatorio')
            isValid = false
          } else if (e.operator === null) {
            this.showNotif('warning', "L'operatore è obbligatorio")
            isValid = false
          }
        }
      })
      if (
        this.badges.length === 1 &&
        this.badges.filter(e => {
          if (e.badgeId !== null && e.operator !== null) {
            return e
          }
        }).length === 0
      ) {
        isValid = false
      }
      return isValid
    },
    askConfirm(message, toExecute, ...args) {
      this.$q
        .dialog({
          title: 'Conferma',
          message: message || 'Sei sicuro di voler procedere',
          cancel: 'Annulla',
          persistent: true
        })
        .onOk(() => {
          toExecute(...args)
        })
    },
    save() {
      if (this.validate()) {
        this.badges = this.badges.filter(e => {
          if (!(e.badgeId === null && e.operator === null)) {
            return e
          }
        })
        const result = this.badges
        if (result.length > 0) {
          let resultFinal = result.filter(el => {
            if (el.operator?.badgeId && el.badgeId !== el.operator.badgeId) {
              return el
            } else if (!el.operator?.badgeId && el.badgeId !== undefined) {
              return el
            }
          })
          resultFinal = resultFinal.map(x => {
            return { badgeId: x.badgeId, operator: x.operator._id.$oid }
          })
          this.checkRemovedBadges(result, resultFinal)
          if (resultFinal.length > 0 && !this.cannotSave) {
            api
              .post('/auth/user/assign', { badge_assignment: resultFinal })
              .then(() => {
                this.showNotif(
                  'positive',
                  'I badge sono stati assegnati/riassegnati correttamente'
                )
                this.getOperators()
              })
              .catch(() => {
                this.showNotif(
                  'negative',
                  'Impossibile assegnare i badge al momento'
                )
              })
          } else {
            this.showNotif(
              'warning',
              'Non è stata effettuata alcuna modifica ai badge'
            )
          }
        } else {
          this.showNotif('warning', 'Non è stato assegnato alcun badge')
        }
      }
    },
    check(e, i) {
      if (e !== null) {
        const res = this.badges.filter((element, index) => {
          if (index !== i) {
            return element
          }
        })
        const element = res.find(x => x.operator._id.$oid === e._id.$oid)
        if (element !== undefined) {
          this.showNotif(
            'warning',
            "L'operatore ha già un badge assegnato ad esso."
          )
          this.badges[i].operator = null
        }
      } else {
        this.badges[this.badges.length - 1].operator = null
      }
    },
    reset() {
      this.dialog = false
      this.role = {
        name: '',
        label: '',
        description: '',
        average_hour_cost: null
      }
    },
    getRoles() {
      api.get('/settings/setting/user/roles').then(response => {
        this.roles = response.data
        this.data_loading = false
      })
    },
    validateRole() {
      if (
        this.role.name.trim() === '' ||
        this.role.label.trim() === '' ||
        this.role.description.trim() === '' ||
        this.role.average_hour_cost === null ||
        this.role.average_hour_cost === ''
      ) {
        return false
      }
      return true
    },
    editRole() {
      if (this.validateRole()) {
        this.role.name = this.role.name.toUpperCase()
        api
          .put('/settings/setting/user/role/' + this.editedId, this.role)
          .then(resp => {
            if (resp.data.success) {
              this.showNotif('positive', 'Ruolo modificato correttamente')
              this.dialog = false
              this.editedId = null
              this.getRoles()
            } else if (resp.data?.msg) {
              this.showNotif('warning', resp.data.msg)
            } else {
              this.showNotif('negative', 'Ruolo non modificato correttamente')
            }
          })
          .catch(error => {
            this.showNotif('negative', 'Ruolo non modificato correttamente')
            this.dialog = false
            this.editedId = null
          })
          .finally(() => {
            this.tab = 'roles'
          })
      }
    },
    addRole() {
      if (this.validateRole()) {
        this.role.name = this.role.name.toUpperCase()
        api
          .post('/settings/setting/user/role', this.role)
          .then(response => {
            if (response.data.success) {
              const msg = 'Ruolo aggiunto correttamente!'
              this.showNotif('positive', msg)
              this.dialog = false
              this.getRoles()
            } else if (!response.data.success && response.data?.msg) {
              this.showNotif('warning', response.data.msg)
            } else {
              this.showNotif('negative', 'Ruolo non aggiunto correttamente')
            }
          })
          .catch(er => {
            this.showNotif('negative', "Errore durante l'aggiunta del ruolo")
            this.dialog = false
          })
          .finally(() => {
            this.tab = 'roles'
          })
      } else {
        this.showNotif('warning', 'Compilare correttamente tutti i campi')
      }
    },
    edit(row) {
      this.dialog = true
      this.editedId = row._id
      this.role = {
        name: row.name,
        label: row.label,
        description: row.description,
        average_hour_cost: row.average_hour_cost.toString()
      }
      this.isEdit = true
    },
    deleteRole(row) {
      api
        .delete('/settings/setting/user/role/' + row._id)
        .then(resp => {
          if (resp.data.success) {
            this.showNotif('positive', 'Ruolo eliminato correttamente.')
            this.getRoles()
          } else {
            this.showNotif(
              'negative',
              "Errore durante l'eliminazione del ruolo."
            )
          }
        })
        .catch(error => {
          this.showNotif('negative', "Errore durante l'eliminazione del ruolo.")
        })
        .finally(() => {
          this.tab = 'roles'
        })
    }
  }
}
</script>
<style>
.q-tabs__content.row.no-wrap.items-center.self-stretch.hide-scrollbar.relative-position.q-tabs__content--align-center {
  display: flex;
  justify-content: flex-start;
  border-bottom: 1px solid lightgrey;
}

.q-tab-panel {
  background: white;
  box-shadow: 0 1px 5px rgb(0 0 0 / 20%), 0 2px 2px rgb(0 0 0 / 14%),
    0 3px 1px -2px rgb(0 0 0 / 12%);
  border-radius: 4px;
  padding-left: 10px;
  padding-right: 10px;
  border: 1px solid lightgrey;
  margin-bottom: 10px;
}
</style>
