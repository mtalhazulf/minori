<template>
  <q-page>
    <div class="row q-mx-xl">
      <Heading :title="'Diario di bordo'" />
    </div>
    <div style="display: flex; align-items: center" class="q-ml-md">
      <q-btn color="secondary" @click="resetDayToToday()">Oggi</q-btn>
      <q-btn color="secondary" class="q-ml-md">
        {{ selectedDay }}
        <q-icon name="event" class="q-ml-md" />
        <q-popup-proxy ref="qDateProxy">
          <q-date
            v-model="selectedDay"
            mask="DD/MM/YYYY"
            :format24h="true"
            :locale="itLocale"
            :options="isDateBeforeToday"
            no-unset
            @update:model-value="
              () => {
                $refs.qDateProxy.hide()
                getLogbook()
              }
            " />
        </q-popup-proxy>
      </q-btn>
    </div>
    <div class="row q-ml-md q-mt-sm">
      <div class="text-h6 q-pb-sm">Mansioni :</div>
      <q-card class="my-card">
        <q-card-section>
          <q-card-section class="q-pt-md">
            <q-list v-if="taken_tasks.length > 0">
              <div v-for="shift in shifts" :key="shift">
                <div class="text-h6 q-pb-sm">{{ shift }} :</div>
                <div
                  v-if="taken_tasks.filter(t => t.shifts === shift).length > 0">
                  <q-item
                    v-for="t in taken_tasks.filter(t => t.shifts === shift)"
                    :key="t._id"
                    style="max-width: 80%"
                    ><div style="width: 100%">
                      <div class="row" style="width: 100%">
                        <q-spinner-hourglass
                          v-if="t.status === 'charged'"
                          class="on-left q-mr-lg q-mt-md"
                          style="font-size: 25px" />
                        <q-icon
                          v-if="t.status === 'done'"
                          name="done"
                          size="30px"
                          class="q-mr-lg q-mt-sm" />
                        <q-item-section>
                          <q-item-label
                            >{{
                              t.task.title.trim().slice(-2) === '||'
                                ? t.task.title.replace('||', '')
                                : t.task.title
                            }}
                          </q-item-label>
                          <q-item-label caption lines="2">
                            {{ t.task.description }}
                          </q-item-label>
                        </q-item-section>
                        <q-item-section
                          v-if="
                            (t.status === 'charged' &&
                              t.operator._id.$oid === operator.uid) ||
                            t['edit']
                          ">
                          <div class="row">
                            <div class="col-3 q-mr-sm justify-end">
                              <q-btn
                                color="green"
                                text-color="white"
                                label="Svolto"
                                @click="
                                  changeStatus(
                                    'notebook',
                                    t.task._id,
                                    true,
                                    null,
                                    convertDateForBackend(selectedDay)
                                  )
                                " />
                            </div>
                            <div class="col-5 justify-start">
                              <q-btn
                                color="red"
                                text-color="white"
                                label="Non Svolto"
                                @click="
                                  changeStatus(
                                    'notebook',
                                    t.task._id,
                                    false,
                                    null,
                                    convertDateForBackend(selectedDay)
                                  )
                                " />
                            </div>
                          </div>
                        </q-item-section>
                        <q-item-section
                          v-else-if="
                            !t['edit'] && t.operator._id.$oid === operator.uid
                          ">
                          <div class="row">
                            <div class="col-3 q-mr-sm justify-end">
                              <q-btn
                                color="white"
                                text-color="black"
                                icon="edit"
                                @click="t['edit'] = true" />
                            </div>
                          </div>
                        </q-item-section>
                        <q-item-section side top>
                          <div class="row">
                            {{
                              typeof t.operator === 'string'
                                ? t.operator
                                : t.operator.name
                                ? t.operator.name + ' ' + t.operator.surname
                                : t.operator.companyName
                            }}
                          </div>
                        </q-item-section>
                      </div>
                      <div
                        v-if="
                          t.operator._id.$oid === operator.uid &&
                          t.status === 'done'
                        "
                        class="row"
                        style="width: 100%">
                        <div class="col-11">
                          <q-item-section caption>
                            <q-input
                              v-model="t['notes']"
                              :readonly="
                                !t['edit'] &&
                                !tasks_ids_just_completed.includes(
                                  t.task._id.$oid
                                )
                              "
                              outlined
                              type="textarea"
                              class="q-ma-sm q-ml-lg"
                              style="width: 100%"
                              label="Aggiungi nota:"
                              maxlength="120"
                              autogrow />
                          </q-item-section>
                        </div>
                        <div class="col-1">
                          <q-item-section
                            caption
                            style="margin-left: 50%; margin-top: 10%">
                            <q-btn
                              color="primary"
                              icon="send"
                              style="width: 10%"
                              size="0.7rem"
                              @click="
                                addTaskNote(
                                  'notebook',
                                  t.task._id,
                                  t['notes'],
                                  t['shifts']
                                )
                              " />
                            <q-btn
                              color="red"
                              icon="delete"
                              style="width: 10%; margin-top: 2px"
                              size="0.7rem"
                              @click="
                                addTaskNote(
                                  'notebook',
                                  t.task._id,
                                  ' ',
                                  t['shifts']
                                )
                              " />
                          </q-item-section>
                        </div>
                      </div>
                      <div
                        v-else-if="
                          t.operator._id.$oid !== operator.uid &&
                          t.status === 'done'
                        "
                        class="row"
                        style="width: 100%; margin-left: 55px">
                        <q-item-section caption style="width: 100%">
                          Nota:
                          <q-item-label caption>{{
                            t?.notes?.trim() ? t.notes : 'Nessuna nota inserita'
                          }}</q-item-label>
                        </q-item-section>
                      </div>
                    </div>
                  </q-item>
                </div>
                <div v-else class="q-pl-md">
                  Nessuna mansione presa in carico al momento
                </div>
              </div>
            </q-list>
            <div v-else class="q-pl-md">
              Nessuna mansione presa in carico al momento
            </div>
          </q-card-section>
        </q-card-section>
      </q-card>
      <div class="text-h6 q-mt-lg q-pb-sm">Consegne :</div>
      <q-card class="my-card q-mb-md">
        <q-card-section>
          <q-card-section class="q-pt-md">
            <q-list v-if="tasks.length > 0">
              <div v-for="shift in shifts" :key="shift">
                <div class="text-h6 q-pb-sm">{{ shift }} :</div>
                <div v-if="tasks.filter(t => t.shift === shift).length > 0">
                  <q-item
                    v-for="task in tasks.filter(t => t.shift === shift)"
                    :key="task._id"
                    style="max-width: 80%"
                    ><div style="width: 100%">
                      <div class="row" style="width: 100%">
                        <q-spinner-hourglass
                          v-if="task.status === 'charged'"
                          class="on-left q-mr-lg q-mt-md"
                          style="font-size: 25px" />
                        <q-icon
                          v-if="task.status === 'done'"
                          name="done"
                          size="30px"
                          class="q-mr-lg q-mt-sm" />
                        <q-item-section>
                          <q-item-label>{{ task.title }}</q-item-label>
                          <q-item-label caption lines="2">
                            {{ task.description }}
                          </q-item-label>
                        </q-item-section>
                        <q-item-section
                          v-if="
                            (task.status === 'charged' &&
                              task.operator._id.$oid === operator.uid) ||
                            task['edit']
                          ">
                          <div class="row">
                            <div class="col-3 q-mr-sm justify-end">
                              <q-btn
                                color="green"
                                text-color="white"
                                label="Svolto"
                                @click="
                                  changeStatus('task', task._id, true, false)
                                " />
                            </div>
                            <div class="col-5 justify-start">
                              <q-btn
                                color="red"
                                text-color="white"
                                label="Non Svolto"
                                @click="
                                  () => {
                                    changeStatus('task', task._id, false, false)
                                  }
                                " />
                            </div>
                          </div>
                        </q-item-section>
                        <q-item-section
                          v-else-if="
                            !task['edit'] &&
                            task.operator._id.$oid === operator.uid
                          ">
                          <div class="row">
                            <div class="col-3 q-mr-sm justify-end">
                              <q-btn
                                color="white"
                                text-color="black"
                                icon="edit"
                                @click="task['edit'] = true" />
                            </div>
                          </div>
                        </q-item-section>
                        <q-item-section side top>
                          <div class="row">
                            {{
                              typeof task.operator === 'string'
                                ? task.operator
                                : task.operator.name
                                ? task.operator.name +
                                  ' ' +
                                  task.operator.surname
                                : task.operator.companyName
                            }}
                          </div>
                        </q-item-section>
                      </div>
                      <div
                        v-if="
                          task.operator._id.$oid === operator.uid &&
                          task.status === 'done'
                        "
                        class="row"
                        style="width: 100%">
                        <div class="col-11">
                          <q-item-section caption
                            ><q-input
                              v-model="task['notes']"
                              :readonly="
                                !task['edit'] &&
                                !tasks_ids_just_completed.includes(
                                  task._id.$oid
                                )
                              "
                              outlined
                              type="textarea"
                              class="q-ma-sm q-ml-lg"
                              style="width: 100%"
                              label="Aggiungi nota:"
                              maxlength="120"
                              autogrow
                          /></q-item-section>
                        </div>
                        <div class="col-1">
                          <q-item-section
                            caption
                            style="margin-left: 50%; margin-top: 10%">
                            <q-btn
                              color="primary"
                              icon="send"
                              style="width: 10%"
                              size="0.7rem"
                              @click="
                                addTaskNote(
                                  'task',
                                  task._id,
                                  task['notes'],
                                  task['shift']
                                )
                              " />
                            <q-btn
                              color="red"
                              icon="delete"
                              style="width: 10%; margin-top: 2px"
                              size="0.7rem"
                              @click="
                                addTaskNote(
                                  'task',
                                  task._id,
                                  ' ',
                                  task['shift']
                                )
                              " />
                          </q-item-section>
                        </div>
                      </div>
                      <div
                        v-else-if="
                          task.operator._id.$oid !== operator.uid &&
                          task.status === 'done'
                        "
                        class="row"
                        style="width: 100%; margin-left: 55px">
                        <q-item-section caption style="width: 100%">
                          Nota:
                          <q-item-label caption>{{
                            task?.notes?.trim()
                              ? task.notes
                              : 'Nessuna nota inserita'
                          }}</q-item-label>
                        </q-item-section>
                      </div>
                    </div>
                  </q-item>
                </div>
                <div v-else class="q-pl-md">
                  Nessuna consegna presa in carico al momento
                </div>
              </div>
            </q-list>
            <div v-else class="q-pl-md">
              Nessuna consegna presa in carico al momento
            </div>
          </q-card-section>
        </q-card-section>
      </q-card>
      <div class="text-h6 q-mt-lg q-pb-sm">Note :</div>
      <q-card class="my-card q-mb-md">
        <q-card-section>
          <q-card-section class="q-pt-md">
            <q-list v-for="shift in shifts" :key="shift">
              <div class="text-h6 q-pb-sm">
                {{ shift }} :
                <div v-if="notes[shift]?.length > 0">
                  <div v-for="nota in notes[shift]" :key="nota">
                    <div class="q-pa-sm q-ml-sm">
                      <div class="row">
                        <div
                          class="col"
                          style="
                            white-space: initial;
                            word-break: break-word;
                            overflow-wrap: break-word;
                          ">
                          <b class="text-body1" style="font-weight: 600"
                            >Nota:</b
                          ><br />
                          <p class="text-body1">
                            {{ nota.notes }}
                          </p>
                        </div>
                        <div class="col q-ml-lg">
                          <b class="text-body1" style="font-weight: 600"
                            >Operatore:</b
                          ><br />
                          <p class="text-body1">
                            {{
                              nota.operator?.companyName
                                ? nota.operator?.companyName
                                : nota.operator?.surname +
                                  ' ' +
                                  nota.operator?.name
                            }}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else class="q-pl-md q-pt-sm text-body1">
                  Nessuna nota inserita al momento
                </div>
              </div>
            </q-list>
          </q-card-section>
        </q-card-section>
      </q-card>

      <q-card class="my-card q-mt-lg q-mb-md">
        <q-card-section>
          <div class="text-h6 q-pl-lg">Nota :</div>
          <q-card-section class="q-pt-md"
            ><q-form class="q-gutter-md" @submit="addNote(note)">
              <q-input
                v-model="note"
                outlined
                type="textarea"
                class="q-ma-sm"
                style="width: 100%"
                label="Aggiungi nota:"
                maxlength="1205" />

              <div
                style="
                  display: flex;
                  align-items: center;
                  justify-content: end;
                ">
                <q-btn type="submit" color="primary" icon="send" />
              </div>
            </q-form>
          </q-card-section>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script>
import Heading from 'components/Heading.vue'
import { api } from 'src/boot/axios'
import { useQuasar } from 'quasar'
import { itLocaleQDate } from 'src/const/QDateItLocale'

export default {
  name: 'Logbook',
  components: {
    Heading
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
      today: new Date().toLocaleDateString('it-IT', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      }),
      selectedDay: {},
      shifts: ['Mattina', 'Pomeriggio', 'Sera'],
      taken_tasks: {},
      tasks_ids_just_completed: [],
      tasks: {},
      operator: {},
      dialog: false,
      selectedTask: null,
      notes: {
        Mattina: [],
        Pomeriggio: [],
        Sera: []
      },
      note: '',
      nextShiftNote: '',
      step: 1,
      notebook_tasks_notes: [],
      tasks_notes: [],
      itLocale: itLocaleQDate
    }
  },
  mounted() {
    this.operator = JSON.parse(sessionStorage.getItem('user'))
    this.selectedDay = this.today
    this.getLogbook()
  },
  methods: {
    getShift() {
      const now = new Date().getHours()
      if (now >= 8 && now < 14) {
        return 'Mattina'
      } else if (now >= 14 && now < 20) {
        return 'Pomeriggio'
      } else {
        return 'Sera'
      }
    },
    isDateBeforeToday(date) {
      return new Date(date) < new Date()
    },
    convertDateForBackend(date) {
      //convert MM/DD/YYYY to YYYY-MM-DD
      return date.split('/').reverse().join('-')
    },
    resetDayToToday() {
      this.selectedDay = this.today
      this.getLogbook()
    },
    getNotebookTasks() {
      api
        .get(
          `tasks/notebook/taken/${this.convertDateForBackend(this.selectedDay)}`
        )
        .then(response => {
          if (response?.data) {
            let newTasks = []
            if (this.notebook_tasks_notes.length > 0) {
              newTasks = response.data.map(element => {
                const el = this.notebook_tasks_notes.find(
                  nota => nota.id?.$oid === element.task?._id.$oid
                )
                return { ...element, notes: el ? el.notes : null }
              })
            } else {
              newTasks = response.data
            }
            this.taken_tasks = newTasks
          }
        })
    },
    getTasks() {
      api
        .get(`tasks/task/taken/${this.convertDateForBackend(this.selectedDay)}`)
        .then(response => {
          if (response?.data) {
            let newTasks = []
            if (this.tasks_notes.length > 0) {
              newTasks = response.data.map(element => {
                const el = this.tasks_notes.find(
                  x =>
                    x.id?.$oid === element._id.$oid ||
                    x._id?.$oid === element._id.$oid
                )
                return { ...element, notes: el ? el.notes : null }
              })
            } else {
              newTasks = response.data
            }
            this.tasks = newTasks
          }
        })
    },
    getLogbook() {
      if (!this.selectedDay) return

      this.notes.Mattina = []
      this.notes.Pomeriggio = []
      this.notes.Sera = []
      this.taken_tasks = []
      this.tasks = []
      this.note = ''
      this.nextShiftNote = ''

      api
        .get(`tasks/logbook/${this.convertDateForBackend(this.selectedDay)}`)
        .then(response => {
          if (response?.data?.length > 0) {
            this.notes.Mattina = response?.data.find(
              n => n.shift === 'Mattina'
            )?.notes
            this.notes.Pomeriggio = response?.data.find(
              n => n.shift === 'Pomeriggio'
            )?.notes
            this.notes.Sera = response?.data.find(
              n => n.shift === 'Sera'
            )?.notes
            this.notebook_tasks_notes = response?.data
              ?.filter(element => element.notebook_tasks)
              .map(element => element.notebook_tasks)
              .flat()
            this.tasks_notes = response?.data
              ?.filter(element => element.tasks)
              .map(element => element.tasks)
              .flat()
          }
          this.getNotebookTasks()
          this.getTasks()
        })
    },
    changeStatus(service, id, accepted, postponed, date) {
      if (postponed && !accepted && this.nextShiftNote.trim() === '') {
        this.showNotif('warning', 'Inserire nota')
      } else {
        const query = { task: id.$oid, isAccepted: accepted }
        if (date) {
          query['date'] = date + ' 00:00:00'
        }
        if (postponed) {
          query['postponed'] = postponed
          query['note'] = this.nextShiftNote
        }
        api
          .put(`/tasks/${service}`, query)
          .then(response => {
            this.showNotif(
              'positive',
              'La ' +
                (service === 'task' ? 'mansione' : 'consegna') +
                ' è stata segnata come ' +
                (accepted
                  ? 'svolta'
                  : 'non svolta, può essere presa in carico da altri operatori.')
            )
            if (accepted) {
              this.tasks_ids_just_completed.push(id.$oid)
            }
            this.getNotebookTasks()
            this.getTasks()
          })
          .catch(er => {
            this.showNotif(
              'negative',
              'Errore durante il cambio stato della ' +
                (service === 'task' ? 'mansione' : 'consegna')
            )
          })
          .finally(() => {
            this.dialog = false
          })
      }
    },
    addNote(note) {
      if (!note.trim()) {
        this.showNotif('warning', 'Campo obbligatorio mancante: Nota')
        return
      }
      api
        .put(`/tasks/logbook`, {
          notes: note,
          date: this.convertDateForBackend(this.selectedDay) + ' 00:00:00',
          shift: this.getShift()
        })
        .then(() => {
          this.showNotif(
            'positive',
            'La nota è stata aggiunta al diario di bordo correttamente.'
          )
          this.getLogbook()
        })
        .catch(() => {
          this.showNotif(
            'negative',
            "Errore durante l'aggiunta della nota al diario di bordo "
          )
        })
      this.note = ''
    },
    addTaskNote(service, id, note, shift) {
      if (note !== undefined) {
        const query = {
          task: id.$oid,
          notes: note
        }
        query['date'] =
          this.convertDateForBackend(this.selectedDay) + ' 00:00:00'
        query['shift'] = shift
        api
          .put(`/tasks/${service}/notes`, query)
          .then(() => {
            this.getLogbook()
            this.showNotif('positive', 'La nota è stata aggiunta')
            this.tasks_ids_just_completed =
              this.tasks_ids_just_completed.filter(x => x !== id.$oid)
          })
          .catch(() => {
            this.showNotif('negative', "Errore durante l'aggiunta della nota")
          })
      }
    }
  }
}
</script>

<style scoped>
.q-card {
  width: 98%;
}

.q-stepper {
  box-shadow: none;
}

.bt-selected {
  background: #26a69a !important;
  color: white !important;
}

.bt-unselected {
  background: white !important;
  color: black !important;
}
</style>
_response_er_response_er_response_er_$event_$event_$event_$event_$event_$event_$event_$event_$event_$event_$event()()()()()
