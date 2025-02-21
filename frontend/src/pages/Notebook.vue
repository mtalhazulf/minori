<template>
  <q-page>
    <div class="row q-mx-xl" style="height: 60px">
      <Heading :title="'Mansionario'" />
    </div>
    <div class="q-pr-md q-pb-md row q-ml-lg q-pl-lg">
      <h5>{{ weekDays[selectedDay] }}</h5>
      <q-space />
      <div style="display: flex; align-items: center">
        <q-btn color="secondary" @click="resetDayToToday()">Oggi</q-btn>
        <q-btn-group v-model="selectedDay" class="q-mr-md q-ml-md">
          <q-btn
            v-for="day in Object.values(dayOfWeek)"
            :key="day"
            :label="day"
            :class="day === selectedDay ? 'bt-selected' : 'bt-unselected'"
            @click="updateDay(day)" />
        </q-btn-group>
        <q-btn
          v-if="operator.usertype !== 'user'"
          color="secondary"
          label="Aggiungi"
          style="width: 90px; height: 40px"
          @click="openDialog()" />
        <q-dialog v-model="dialog">
          <q-card style="max-width: 80vw">
            <q-card-section>
              <div class="text-h6">Nuova mansione</div>
            </q-card-section>

            <q-card-section class="q-pt-none">
              <form class="q-my-sm">
                <q-select
                  v-model="selectedTaskType"
                  :options="settingsTasks.map(task => task.label)"
                  outlined
                  label="Tipologia"
                  class="q-my-sm" />
                <q-select
                  v-model="selectedTaskModule"
                  :disable="selectedTaskType === '' || !modules.length"
                  :options="modules"
                  outlined
                  label="Modulo"
                  class="q-my-sm" />
                <div class="text-h7 q-mt-md q-mb-xs">
                  Giorni e turni della mansione
                </div>
                <WeeklyCheckboxCalendar
                  :dayofweek="dayOfWeek"
                  @periods="value => (task.periods = value)" />
                <q-input
                  v-model="task.description"
                  outlined
                  label="Descrizione"
                  type="textarea"
                  class="q-my-md" />
              </form>
            </q-card-section>

            <q-card-actions align="right">
              <q-btn
                v-close-popup
                flat
                label="Cancella"
                color="primary"
                @click="resetForm()" />
              <q-btn label="Aggiungi" color="primary" @click="addTask()" />
            </q-card-actions>
          </q-card>
        </q-dialog>
      </div>

      <div style="display: flex; align-items: center">
        <q-dialog v-model="info_dialog">
          <q-card>
            <q-card-section>
              <div class="text-h6">Dettagli mansione</div>
            </q-card-section>

            <q-card-section class="q-pt-none">
              <div style="max-width: 350px">
                <q-list>
                  <q-item>
                    <q-item-section>
                      <q-item-label overline>Tipologia</q-item-label>
                      <q-item-label lines="2">
                        {{ selectedTask.type }}
                      </q-item-label>
                    </q-item-section>
                  </q-item>

                  <q-separator spaced inset />

                  <q-list v-if="selectedTask.module">
                    <q-item>
                      <q-item-section>
                        <q-item-label overline>Modulo</q-item-label>
                        <q-item-label lines="2">
                          {{ selectedTask.module }}
                        </q-item-label>
                      </q-item-section>
                    </q-item>

                    <q-separator spaced inset />
                  </q-list>
                  <q-list v-if="selectedTask.description">
                    <q-item>
                      <q-item-section>
                        <q-item-label overline>Descrizione</q-item-label>
                        <q-item-label>{{
                          selectedTask.description
                        }}</q-item-label>
                      </q-item-section>
                    </q-item>

                    <q-separator spaced inset />
                  </q-list>
                  <q-item>
                    <q-item-section>
                      <q-item-label overline
                        >Pianificazione settimanale</q-item-label
                      >
                      <q-item-label v-for="taskS in tasksGroup" :key="taskS">
                        {{
                          dayOfWeekInverted[taskS.dayofweek] +
                          ' - ' +
                          taskS.shifts
                        }}
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-separator spaced inset />

                  <q-item>
                    <q-item-section>
                      <q-item-label
                        >Status :
                        <q-badge
                          rounded
                          :color="labelcolors[selectedTask.status]"
                          :label="labelTexts[selectedTask.status]" />
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                  <div
                    v-if="
                      (selectedTask.status === 'charged' ||
                        selectedTask.status === 'done') &&
                      selectedTask.operator &&
                      selectedTask.operator.name &&
                      selectedTask.operator.surname
                    ">
                    <q-separator spaced inset />

                    <q-item>
                      <q-item-section>
                        <q-item-label overline>Operatore </q-item-label>
                        <q-item-label>{{
                          selectedTask.operator?.name +
                          ' ' +
                          selectedTask.operator?.surname
                        }}</q-item-label>
                      </q-item-section>
                    </q-item>
                  </div>
                </q-list>
              </div>
            </q-card-section>

            <q-card-actions align="right">
              <q-btn
                v-close-popup
                flat
                label="Chiudi"
                color="primary"
                @click="info_dialog = false" />
            </q-card-actions>
          </q-card>
        </q-dialog>
      </div>

      <q-stepper
        ref="stepper"
        v-model="step"
        header-nav
        color="primary"
        animated
        @update:model-value="updateTasks()">
        <q-step :name="1" title="Mattino" icon="settings" :done="done1">
          <q-table
            v-model:selected="selected"
            v-model:pagination="pagination"
            title="Mansioni turno mattina"
            :rows="tasks"
            :columns="columns"
            row-key="title"
            selection="multiple"
            :filter="filter"
            grid
            hide-header
            :loading="data_loading">
            <template #item="props">
              <div
                class="q-pa-xs col-xs-12 col-sm-6 col-md-4 col-lg-3 grid-style-transition"
                :style="
                  (props.row.selected || props.selected) &&
                  props.row.status !== 'done'
                    ? 'transform: scale(0.95);'
                    : ''
                ">
                <q-card
                  :class="
                    props.row.status === 'charged'
                      ? 'bg-charged'
                      : props.row.status === 'done'
                      ? 'bg-done'
                      : ''
                  "
                  :style="{
                    height: auto
                  }">
                  <q-card-section>
                    <div class="row">
                      <div class="col">
                        <q-checkbox
                          v-if="
                            operator.usertype !== 'admin' &&
                            operator.usertype !== 'superadmin' &&
                            props.row.status !== 'done' &&
                            selectedDay === todayDayName &&
                            (props.row.operator === undefined ||
                              props.row.operator.$oid === operator.uid)
                          "
                          v-model="props.row.selected"
                          dense
                          :label="
                            props.row.type.length > 20
                              ? props.row.type.substring(0, 16) + '...'
                              : props.row.type
                          "
                          @update:model-value="add($event, props.row)" />
                        <template v-else>
                          <p style="margin-bottom: 0px; font-size: 1.1em">
                            {{
                              props.row.type.length > 20
                                ? props.row.type.substring(0, 16) + '...'
                                : props.row.type
                            }}
                          </p>
                          <p>
                            {{
                              props.row.module.length > 20
                                ? props.row.module.substring(0, 16) + '...'
                                : props.row.module
                            }}
                          </p>
                        </template>
                      </div>
                      <div class="col-2">
                        <q-icon
                          size="2em"
                          name="visibility"
                          style="color: #1976d2"
                          @click="getInfo(props.row)" />
                      </div>
                      <div
                        v-if="
                          operator.usertype === 'admin' ||
                          operator.usertype === 'superadmin'
                        "
                        class="col-2">
                        <q-icon
                          size="1.8em"
                          name="delete"
                          style="color: #f63333db"
                          @click="
                            askConfirm(
                              strings.deleteMansione,
                              deleteTask,
                              props.row
                            )
                          " />
                      </div>
                    </div>
                  </q-card-section>
                  <q-separator />
                  <q-list
                    v-if="props.row.description.length"
                    dense
                    class="q-pt-sm q-pb-md">
                    <q-item>
                      <q-item-section>
                        <q-item-label>Descrizione:</q-item-label>
                        <q-item-label caption lines="2">{{
                          props.row.description
                        }}</q-item-label>
                      </q-item-section>
                    </q-item>
                  </q-list>
                </q-card>
              </div>
            </template>
            <template #bottom="scope">
              <q-btn
                v-if="scope.pagesNumber > 2"
                icon="first_page"
                color="grey-8"
                round
                dense
                flat
                :disable="scope.isFirstPage"
                @click="scope.firstPage" />

              <q-btn
                icon="chevron_left"
                color="grey-8"
                round
                dense
                flat
                :disable="scope.isFirstPage"
                @click="scope.prevPage" />

              {{ scope.pagination.page }} di {{ scope.pagesNumber }}
              <q-btn
                icon="chevron_right"
                color="grey-8"
                round
                dense
                flat
                :disable="scope.isLastPage"
                @click="scope.nextPage" />

              <q-btn
                v-if="scope.pagesNumber > 2"
                icon="last_page"
                color="grey-8"
                round
                dense
                flat
                :disable="scope.isLastPage"
                @click="scope.lastPage" />
              <q-space />
              <q-btn
                v-if="
                  operator.usertype !== 'admin' &&
                  operator.usertype !== 'superadmin'
                "
                color="secondary"
                :loading="loading"
                :disable="selected.length <= 0 && unselected.length <= 0"
                style="width: 150px"
                @click="takeCharge()">
                {{
                  selected.length > 0 && unselected.length > 0
                    ? 'Prendi in carico ' +
                      selected.length +
                      ' e lascia ' +
                      unselected.length
                    : selected.length > 0
                    ? 'Prendi in carico ' + selected.length
                    : unselected.length > 0
                    ? 'Lascia ' + unselected.length
                    : 'Prendi in carico'
                }}
                <template #loading>
                  <q-spinner-hourglass class="on-left" />
                  Loading...
                </template>
              </q-btn>
            </template>
            <template #no-data="{ message }">
              <div class="full-width row flex-center text-primary q-gutter-sm">
                <div v-if="message === 'Loading...'">{{ message }}</div>
                <div v-else>
                  <q-icon size="2em" name="sentiment_dissatisfied" />
                  <span>
                    {{
                      errDataMsg
                        ? 'Impossibile caricare le mansioni al momento. Prova a ricaricare la pagina o a verificare che il dispositivo sia connessso alla rete internet.'
                        : 'Nessuna mansione presente ...'
                    }}
                  </span>
                </div>
              </div>
            </template>
          </q-table>
        </q-step>
        <q-step
          :name="2"
          title="Pomeriggio"
          caption=""
          icon="settings"
          :done="done2">
          <q-table
            v-model:selected="selected"
            v-model:pagination="pagination"
            grid
            title="Mansioni turno pomeriggio"
            :rows="tasks"
            :columns="columns"
            row-key="title"
            selection="multiple"
            :filter="filter"
            hide-header
            :loading="data_loading">
            <template #item="props">
              <div
                class="q-pa-xs col-xs-12 col-sm-6 col-md-4 col-lg-3 grid-style-transition"
                :style="
                  (props.row.selected || props.selected) &&
                  props.row.status !== 'done'
                    ? 'transform: scale(0.95);'
                    : ''
                ">
                <q-card
                  :class="
                    props.row.status === 'charged'
                      ? 'bg-charged'
                      : props.row.status === 'done'
                      ? 'bg-done'
                      : ''
                  "
                  :style="{
                    height: auto
                  }">
                  <q-card-section
                    :style="{
                      'padding-bottom': '10px'
                    }"
                    ><div class="row">
                      <div class="col">
                        <q-checkbox
                          v-if="
                            operator.usertype !== 'admin' &&
                            operator.usertype !== 'superadmin' &&
                            props.row.status !== 'done' &&
                            selectedDay === todayDayName &&
                            (props.row.operator === undefined ||
                              props.row.operator.$oid === operator.uid)
                          "
                          v-model="props.row.selected"
                          style="margin-bottom: 10px"
                          dense
                          @update:model-value="add($event, props.row)">
                          <q-item-label>{{
                            props.row.type.length > 20
                              ? props.row.type.substring(0, 16) + '...'
                              : props.row.type
                          }}</q-item-label>
                          <q-item-label caption>
                            {{
                              props.row.module.length > 20
                                ? props.row.module.substring(0, 16) + '...'
                                : props.row.module
                            }}
                          </q-item-label>
                        </q-checkbox>
                        <template v-else>
                          <p style="margin-bottom: 0px; font-size: 1.1em">
                            {{
                              props.row.type.length > 20
                                ? props.row.type.substring(0, 16) + '...'
                                : props.row.type
                            }}
                          </p>
                          <p>
                            {{
                              props.row.module.length > 20
                                ? props.row.module.substring(0, 16) + '...'
                                : props.row.module
                            }}
                          </p>
                        </template>
                      </div>
                      <div class="col-2">
                        <q-icon
                          size="2em"
                          name="visibility"
                          style="color: #1976d2"
                          @click="getInfo(props.row)" />
                      </div>
                      <div
                        v-if="
                          operator.usertype === 'admin' ||
                          operator.usertype === 'superadmin'
                        "
                        class="col-2">
                        <q-icon
                          size="1.8em"
                          name="delete"
                          style="color: #f63333db"
                          @click="
                            askConfirm(
                              strings.deleteMansione,
                              deleteTask,
                              props.row
                            )
                          " />
                      </div>
                    </div>
                  </q-card-section>
                  <q-separator />
                  <q-list
                    v-if="props.row.description.length"
                    dense
                    class="q-pt-sm q-pb-md">
                    <q-item>
                      <q-item-section>
                        <q-item-label>Descrizione:</q-item-label>
                        <q-item-label caption lines="2">{{
                          props.row.description
                        }}</q-item-label>
                      </q-item-section>
                    </q-item>
                  </q-list>
                </q-card>
              </div>
            </template>
            <template #bottom="scope">
              <q-btn
                v-if="scope.pagesNumber > 2"
                icon="first_page"
                color="grey-8"
                round
                dense
                flat
                :disable="scope.isFirstPage"
                @click="scope.firstPage" />

              <q-btn
                icon="chevron_left"
                color="grey-8"
                round
                dense
                flat
                :disable="scope.isFirstPage"
                @click="scope.prevPage" />

              {{ scope.pagination.page }} di {{ scope.pagesNumber }}
              <q-btn
                icon="chevron_right"
                color="grey-8"
                round
                dense
                flat
                :disable="scope.isLastPage"
                @click="scope.nextPage" />

              <q-btn
                v-if="scope.pagesNumber > 2"
                icon="last_page"
                color="grey-8"
                round
                dense
                flat
                :disable="scope.isLastPage"
                @click="scope.lastPage" />
              <q-space />
              <q-btn
                v-if="
                  operator.usertype !== 'admin' &&
                  operator.usertype !== 'superadmin'
                "
                color="secondary"
                :loading="loading"
                :disable="
                  (selected.length <= 0 && unselected.length <= 0) ||
                  todayDayName !== selectedDay
                "
                style="width: 150px"
                @click="takeCharge()">
                {{
                  selected.length > 0 && unselected.length > 0
                    ? 'Prendi in carico ' +
                      selected.length +
                      ' e lascia ' +
                      unselected.length
                    : selected.length > 0
                    ? 'Prendi in carico ' + selected.length
                    : unselected.length > 0
                    ? 'Lascia ' + unselected.length
                    : 'Prendi in carico'
                }}
                <template #loading>
                  <q-spinner-hourglass class="on-left" />
                  Loading...
                </template>
              </q-btn>
            </template>
            <template #no-data="{ message }">
              <div class="full-width row flex-center text-primary q-gutter-sm">
                <div v-if="message === 'Loading...'">{{ message }}</div>
                <div v-else>
                  <q-icon size="2em" name="sentiment_dissatisfied" />
                  <span>
                    {{
                      errDataMsg
                        ? 'Impossibile caricare le mansioni al momento. Prova a ricaricare la pagina o a verificare che il dispositivo sia connessso alla rete internet.'
                        : 'Nessuna mansione presente ...'
                    }}
                  </span>
                </div>
              </div>
            </template>
          </q-table>
        </q-step>

        <q-step :name="3" title="Sera" icon="settings" :done="done3">
          <q-table
            v-model:selected="selected"
            v-model:pagination="pagination"
            title="Mansioni turno sera"
            :rows="tasks"
            :columns="columns"
            row-key="title"
            selection="multiple"
            :filter="filter"
            grid
            hide-header
            :loading="data_loading">
            <template #item="props">
              <div
                class="q-pa-xs col-xs-12 col-sm-6 col-md-4 col-lg-3 grid-style-transition"
                :style="
                  (props.row.selected || props.selected) &&
                  props.row.status !== 'done'
                    ? 'transform: scale(0.95);'
                    : ''
                ">
                <q-card
                  :class="
                    props.row.status === 'charged'
                      ? 'bg-charged'
                      : props.row.status === 'done'
                      ? 'bg-done'
                      : ''
                  "
                  :style="{
                    height: auto
                  }">
                  <q-card-section
                    :style="{
                      'padding-bottom': '0px'
                    }">
                    <div class="row">
                      <div class="col">
                        <q-checkbox
                          v-if="
                            operator.usertype !== 'admin' &&
                            operator.usertype !== 'superadmin' &&
                            props.row.status !== 'done' &&
                            selectedDay === todayDayName &&
                            (props.row.operator === undefined ||
                              props.row.operator.$oid === operator.uid)
                          "
                          v-model="props.row.selected"
                          dense
                          :label="
                            props.row.title.length > 20
                              ? props.row.title.substring(0, 16) + '...'
                              : props.row.title
                          "
                          @update:model-value="add($event, props.row)" />
                        <template v-else>
                          <p style="margin-bottom: 0px; font-size: 1.1em">
                            {{
                              props.row.type.length > 20
                                ? props.row.type.substring(0, 16) + '...'
                                : props.row.type
                            }}
                          </p>
                          <p>
                            {{
                              props.row.module.length > 20
                                ? props.row.module.substring(0, 16) + '...'
                                : props.row.module
                            }}
                          </p>
                        </template>
                      </div>
                      <div class="col-2">
                        <q-icon
                          size="2em"
                          name="visibility"
                          style="color: #1976d2"
                          @click="getInfo(props.row)" />
                      </div>
                      <div
                        v-if="
                          operator.usertype === 'admin' ||
                          operator.usertype === 'superadmin'
                        "
                        class="col-2">
                        <q-icon
                          size="1.8em"
                          name="delete"
                          style="color: #f63333db"
                          @click="
                            askConfirm(
                              strings.deleteMansione,
                              deleteTask,
                              props.row
                            )
                          " />
                      </div>
                    </div>
                  </q-card-section>
                  <q-separator />

                  <q-list
                    v-if="props.row.description.length"
                    dense
                    class="q-pt-sm q-pb-md">
                    <q-item>
                      <q-item-section>
                        <q-item-label>Descrizione:</q-item-label>
                        <q-item-label caption lines="2">{{
                          props.row.description
                        }}</q-item-label>
                      </q-item-section>
                    </q-item>
                  </q-list>
                </q-card>
              </div>
            </template>
            <template #bottom="scope">
              <q-btn
                v-if="scope.pagesNumber > 2"
                icon="first_page"
                color="grey-8"
                round
                dense
                flat
                :disable="scope.isFirstPage"
                @click="scope.firstPage" />

              <q-btn
                icon="chevron_left"
                color="grey-8"
                round
                dense
                flat
                :disable="scope.isFirstPage"
                @click="scope.prevPage" />

              {{ scope.pagination.page }} di {{ scope.pagesNumber }}
              <q-btn
                icon="chevron_right"
                color="grey-8"
                round
                dense
                flat
                :disable="scope.isLastPage"
                @click="scope.nextPage" />

              <q-btn
                v-if="scope.pagesNumber > 2"
                icon="last_page"
                color="grey-8"
                round
                dense
                flat
                :disable="scope.isLastPage"
                @click="scope.lastPage" />
              <q-space />
              <q-btn
                v-if="
                  operator.usertype !== 'admin' &&
                  operator.usertype !== 'superadmin'
                "
                color="secondary"
                :loading="loading"
                :disable="selected.length <= 0 && unselected.length <= 0"
                style="width: 150px"
                @click="takeCharge()">
                {{
                  selected.length > 0 && unselected.length > 0
                    ? 'Prendi in carico ' +
                      selected.length +
                      ' e lascia ' +
                      unselected.length
                    : selected.length > 0
                    ? 'Prendi in carico ' + selected.length
                    : unselected.length > 0
                    ? 'Lascia ' + unselected.length
                    : 'Prendi in carico'
                }}
                <template #loading>
                  <q-spinner-hourglass class="on-left" />
                  Loading...
                </template>
              </q-btn>
            </template>
            <template #no-data="{ message }">
              <div class="full-width row flex-center text-primary q-gutter-sm">
                <div v-if="message === 'Loading...'">{{ message }}</div>
                <div v-else>
                  <q-icon size="2em" name="sentiment_dissatisfied" />
                  <span>
                    {{
                      errDataMsg
                        ? 'Impossibile caricare le mansioni al momento. Prova a ricaricare la pagina o a verificare che il dispositivo sia connessso alla rete internet.'
                        : 'Nessuna mansione presente ...'
                    }}
                  </span>
                </div>
              </div>
            </template>
          </q-table>
        </q-step>
      </q-stepper>
    </div>
  </q-page>
</template>

<script>
import Heading from 'components/Heading.vue'
import WeeklyCheckboxCalendar from 'src/components/WeeklyCheckboxCalendar.vue'
import { useQuasar } from 'quasar'
import { api } from 'src/boot/axios'

export default {
  name: 'Notebook',
  components: {
    Heading,
    WeeklyCheckboxCalendar
  },
  setup() {
    const $q = useQuasar()

    return {
      showNotif(tp, msg) {
        $q.notify({
          type: tp,
          message: msg,
          position: 'top-right',
          timeout: 1000
        })
      }
    }
  },
  data() {
    return {
      step: 1,
      done1: false,
      done2: false,
      done3: false,
      filter: '',
      selected: [],
      firstLevelSettingTask: [],
      secondLevelSettingTask: [],
      labelcolors: {
        disabled: 'grey-8',
        active: 'primary',
        done: 'positive',
        charged: 'warning'
      },
      labelTexts: {
        disabled: 'Disabilitato',
        active: 'Da svolgere',
        done: 'Svolta',
        charged: 'Presa in carico'
      },
      columns: [
        {
          name: 'name',
          required: true,
          label: 'Mansione',
          align: 'center',
          field: 'name',
          sortable: true
        },
        {
          name: 'description',
          align: 'center',
          label: 'Descrizione',
          field: 'description',
          sortable: true
        }
      ],
      tasks: [],
      settingsTasks: [],
      tasksGroup: [],
      operator: '',
      todayDayName: new Date().toLocaleDateString('it-IT', {
        weekday: 'short'
      }),
      selectedDay: '',
      selectedTaskType: '',
      selectedTaskModule: '',
      modules: [],
      weekDays: {},
      weekDaysBacked: {}, // formatted YYYY-MM-DD
      loading: false,
      data_loading: true,
      shift: '',
      unselected: [],
      dialog: false,
      options: ['Mattina', 'Pomeriggio', 'Sera'],
      dayOfWeek: {
        Lunedì: 'lun',
        Martedì: 'mar',
        Mercoledì: 'mer',
        Giovedì: 'gio',
        Venerdì: 'ven',
        Sabato: 'sab',
        Domenica: 'dom'
      },
      dayOfWeekInverted: {
        lun: 'Lunedì',
        mar: 'Martedì',
        mer: 'Mercoledì',
        gio: 'Giovedì',
        ven: 'Venerdì',
        sab: 'Sabato',
        dom: 'Domenica'
      },
      task: {
        title: '',
        description: '',
        periods: []
      },
      pagination: {
        page: 0,
        rowsPerPage: 8
      },
      errDataMsg: false,
      minors: [],
      info_dialog: false,
      selectedTask: {},
      strings: {
        deleteMansione: 'Sei sicuro di voler eliminare la mansione?'
      }
    }
  },
  watch: {
    selectedTaskType: function () {
      this.modules = this.settingsTasks
        .find(task => task.label === this.selectedTaskType)
        ?.modules?.map(module => module.label)
      this.selectedTaskModule = ''
    }
  },
  mounted() {
    this.operator = JSON.parse(sessionStorage.getItem('user'))
    this.selectedDay = this.todayDayName
    if (this.operator !== 'admin') this.getSettingsTasks()
    this.weekDays = this.getWeekDays(false)
    this.weekDaysBacked = this.getWeekDays(true)
    this.checkShift()
  },
  methods: {
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
    getTasksGroup(taskTitle) {
      api
        .get(`/tasks/notebook/type/${encodeURIComponent(taskTitle)}`)
        .then(res => {
          const group = res.data
          const daysOfWeek = ['lun', 'mar', 'mer', 'gio', 'ven', 'sab', 'dom']
          group.sort((a, b) => {
            const dayIndexA = daysOfWeek.indexOf(a.dayofweek[0])
            const dayIndexB = daysOfWeek.indexOf(b.dayofweek[0])
            if (dayIndexA === dayIndexB) {
              return a.shifts[0].localeCompare(b.shifts[0])
            }
            return dayIndexA - dayIndexB
          })
          this.tasksGroup = group
          return
        })
    },
    resetDayToToday() {
      this.selectedDay = this.todayDayName
      this.getMansioni()
    },
    updateDay(day) {
      this.selected = []
      this.unselected = []
      this.selectedDay = day
      this.getMansioni()
    },
    getWeekDays(isBacked = false) {
      const today = new Date()
      const dayOfWeek = today.getDay()
      const firstDayOfWeek = new Date(
        today.getFullYear(),
        today.getMonth(),
        today.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1)
      )
      const daysOfWeek = {}
      const days = Object.values(this.dayOfWeek)
      for (let i = 0; i < days.length; i++) {
        const day = new Date(firstDayOfWeek.getTime() + i * 24 * 60 * 60 * 1000)
        if (isBacked) {
          daysOfWeek[days[i]] = day
            .toLocaleDateString('it-IT', {
              year: 'numeric',
              month: '2-digit',
              day: '2-digit'
            })
            .split('/')
            .reverse()
            .join('-')
        } else {
          daysOfWeek[days[i]] = day.toLocaleDateString('it-IT', {
            day: 'numeric',
            month: 'long'
          })
        }
      }
      return daysOfWeek
    },
    check() {
      if (this.selected.length <= 0 && this.unselected.length <= 0) {
        return true
      } else {
        return false
      }
    },
    getSettingsTasks() {
      this.data_loading = true
      api
        .get('/settings/setting/task')
        .then(response => {
          this.settingsTasks = response.data
          this.data_loading = false
        })
        .catch(er => {
          this.errDataMsg = true
          this.data_loading = false
        })
    },
    takeCharge() {
      const steps = ['Mattina', 'Pomeriggio', 'Sera']

      const charging_request = {
        charge: this.selected.map(function (el) {
          return el._id.$oid
        }),
        discharge: this.unselected.map(function (el) {
          return el._id.$oid
        })
      }

      this.loading = true
      api
        .post(
          '/tasks/notebook/' +
            steps[this.step - 1] +
            '/' +
            this.selectedDay +
            '/' +
            this.weekDaysBacked[this.selectedDay],
          charging_request
        )
        .then(response => {
          this.loading = false
          api.post('/auth/log', {
            name: 'Presa in carico',
            description: 'Mansione: presa in carico'
          })
          this.showNotif(
            'positive',
            'Le mansioni sono state prese in carico o lasciate correttamente.'
          )
          setTimeout(() => {
            this.$router.go(0)
          }, 1000)
        })
        .catch(er => {
          this.loading = false
          this.showNotif(
            'negative',
            "E' stato riscontrato un errore durante la presa in carico o il rilascio delle mansioni."
          )
        })
    },
    getMansioni(shift = ['Mattina', 'Pomeriggio', 'Sera'][this.step - 1]) {
      api
        .get(
          '/tasks/notebook/' +
            shift +
            '/' +
            this.selectedDay +
            '/' +
            this.weekDaysBacked[this.selectedDay]
        )
        .then(response => {
          this.tasks = response.data.map(task => {
            return {
              ...task,
              type: task.title.includes('||')
                ? task.title.split('||')[0].trim()
                : task.title,
              module: task.title.includes('||')
                ? task.title.split('||')[1].trim()
                : ''
            }
          })
          setTimeout(() => {
            this.errDataMsg = false
            this.data_loading = false
          }, 500)
        })
        .catch(() => {
          this.errDataMsg = true
          this.data_loading = false
        })
    },
    checkShift() {
      const now = new Date().getHours()
      if (now >= 8 && now < 14) {
        this.shift = 'Mattina'
        this.getMansioni(this.shift)
        this.step = 1
      } else if (now >= 14 && now < 20) {
        this.shift = 'Pomeriggio'
        this.getMansioni(this.shift)
        this.step = 2
      } else {
        this.shift = 'Sera'
        this.getMansioni(this.shift)
        this.step = 3
      }
    },
    updateTasks() {
      this.data_loading = true
      this.getMansioni()
    },
    deleteTask(task) {
      const steps = ['Mattina', 'Pomeriggio', 'Sera']
      api
        .delete(
          '/tasks/notebook/' +
            steps[this.step - 1] +
            '/' +
            this.selectedDay +
            '/' +
            task._id.$oid
        )
        .then(response => {
          this.showNotif(
            'positive',
            'La mansione è stata eliminata correttamente.'
          )
          this.getMansioni()
        })
        .catch(er => {
          this.showNotif('negative', 'Impossibile eliminare la mansione')
        })
    },
    add(e, row) {
      if (e) {
        if (this.unselected.find(e => e._id.$oid === row._id.$oid)) {
          this.unselected = this.unselected.filter(e => {
            return e._id.$oid !== row._id.$oid
          })
        } else {
          this.selected.push(row)
        }
      } else if (!e) {
        if (this.selected.find(e => e._id.$oid === row._id.$oid)) {
          this.selected = this.selected.filter(e => {
            return e._id.$oid !== row._id.$oid
          })
        } else {
          this.unselected.push(row)
        }
      }
    },
    resetForm() {
      this.task = {
        title: '',
        description: '',
        periods: []
      }
      this.selectedTaskModule = ''
      this.selectedTaskType = ''
    },
    openDialog() {
      this.resetForm()
      api.get('/minors/minor/all').then(response => {
        this.minors = response.data
      })
      this.dialog = true
    },
    close(ref) {
      this.$refs[ref].hidePopup()
    },
    validate() {
      let isValid = true
      const fields = {
        title: 'Tipologia',
        description: 'Descrizione',
        periods: 'Giorni e turni della mansione'
      }
      for (const [key, value] of Object.entries(this.task)) {
        if (
          key !== 'title' &&
          (typeof value === 'object' || typeof value === Array) &&
          value.length === 0
        ) {
          this.showNotif(
            'warning',
            'Il campo ' + fields[key] + ' deve essere inserito.'
          )
          isValid = false
        }
        if (this.selectedTaskType === '') {
          this.showNotif(
            'warning',
            'I campi Tipologia e Modulo devono essere inseriti.'
          )
          isValid = false
        }
      }
      // this.formatTitle(this.task.title)
      return isValid
    },
    // formatTitle(toFormat) {
    //   const str = toFormat.toLowerCase()
    //   const toCapitalize = str.charAt(0).toUpperCase()
    //   this.task.title = toCapitalize + '' + str.slice(1)
    // },
    addTask() {
      if (this.validate()) {
        const formattedTask = {
          ...this.task,
          description: this.task.description.trim(),
          title: `${this.selectedTaskType} || ${this.selectedTaskModule}`,
          periods: this.task.periods.map(e => {
            return {
              dayofweek: e.split('-')[0],
              shift: e.split('-')[1]
            }
          })
        }
        api
          .post('/tasks/notebook', formattedTask)
          .then(response => {
            this.showNotif(
              'positive',
              'La mansione è stata aggiunta correttamente.'
            )
            this.data_loading = true
            this.checkShift()
          })
          .then(() => {
            this.dialog = false
          })
          .catch(() => {
            this.showNotif(
              'negative',
              'Impossibile aggiungere la mansione, controlla che non sia già presente.'
            )
          })
      }
    },
    getInfo(task) {
      this.getTasksGroup(task.title)
      this.selectedTask = task
      this.info_dialog = true
    }
  }
}
</script>

<style scoped>
h5 {
  margin-top: 20px;
  margin-bottom: 20px;
}

.q-stepper--horizontal .q-stepper__step-inner {
  padding-top: 0%;
}

.q-stepper.q-stepper--horizontal {
  width: 100%;
}

@media (min-width: 600px) {
  .q-dialog__inner--minimized > div {
    min-width: 306px;
  }
}

.q-icon {
  cursor: pointer;
}

.bg-selected {
  background: #b5f77561 !important;
  border: 1px solid darkseagreen;
}

.bt-selected {
  background: #26a69a !important;
  color: white !important;
}

.bg-charged {
  background: rgba(255, 255, 102, 0.5) !important;
  color: black !important;
}

.bg-done {
  background: rgba(102, 255, 102, 0.5) !important;
  color: black !important;
}

.bt-unselected {
  background: white !important;
  color: black !important;
}
</style>
