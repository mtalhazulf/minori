<template>
  <q-page class="q-mx-xl">
    <div class="row"><Heading :title="'Scheda informativa adulto'" /></div>
    <div class="row">
      <q-card style="width: 100%"
        ><div class="q-pa-md">
          <q-form class="q-gutter-md col" @submit="onSubmit">
            <div class="row text-center justify-center">INFO COMUNITA'</div>
            <div class="row">
              <q-input
                v-model="adult_info_sheet.community.name"
                outlined
                label="Comunità "
                class="q-ma-sm"
                maxlength="58" />
              <q-input
                v-model="adult_info_sheet.community.address"
                outlined
                label="Via "
                class="q-ma-sm"
                maxlength="33" />
              <q-input
                v-model="adult_info_sheet.community.county"
                outlined
                label="Prov. "
                class="q-ma-sm"
                maxlength="19" />
              <q-input
                v-model="adult_info_sheet.community.municipality"
                outlined
                label="Comune "
                class="q-ma-sm"
                maxlength="33" />
              <q-input
                v-model="adult_info_sheet.community.phone_number"
                outlined
                label="Tel. "
                maxlength="15"
                type="tel"
                class="q-ma-sm" />
            </div>
            <div class="row text-center justify-center">INFO ADULTO</div>
            <div class="row">
              <q-input
                v-model="adult_info_sheet.adult.surname"
                outlined
                label="Cognome "
                class="q-ma-sm"
                maxlength="26"
                :disable="true" />
              <q-input
                v-model="adult_info_sheet.adult.name"
                outlined
                label="Nome "
                class="q-ma-sm"
                maxlength="26"
                :disable="true" />
              <q-input
                v-model="adult_info_sheet.adult.birthdate"
                outlined
                class="q-ma-sm"
                label="Nato/a il: "
                readonly>
                <template #append>
                  <q-icon name="event" class="cursor-pointer">
                    <q-popup-proxy
                      ref="qDateProxy"
                      cover
                      transition-show="scale"
                      transition-hide="scale">
                      <q-date
                        type="date"
                        :options="optionsFn"
                        @update:model-value="
                          (value, reason, detail) => {
                            watchDate(value, 'birthdate')
                          }
                        ">
                        <div class="row items-center justify-end">
                          <q-btn
                            v-close-popup
                            label="Close"
                            color="primary"
                            flat />
                        </div>
                      </q-date>
                    </q-popup-proxy>
                  </q-icon>
                </template>
              </q-input>
              <q-input
                v-model="adult_info_sheet.adult.birthplace"
                outlined
                label="a "
                class="q-ma-sm"
                maxlength="29" />
            </div>
            <div class="row">
              <q-input
                v-model="adult_info_sheet.adult.resident"
                outlined
                label="Residente "
                class="q-ma-sm"
                maxlength="42" />
              <q-input
                v-model="adult_info_sheet.adult.county"
                outlined
                label="Prov. "
                class="q-ma-sm"
                maxlength="15" />
              <q-input
                v-model="adult_info_sheet.adult.paternity"
                outlined
                label="Paternità "
                class="q-ma-sm"
                maxlength="38" />
              <q-input
                v-model="adult_info_sheet.adult.paternity_residence"
                outlined
                label="Res. "
                class="q-ma-sm"
                maxlength="38" />
            </div>
            <div class="row">
              <q-input
                v-model="adult_info_sheet.adult.maternity"
                outlined
                label="Maternità "
                class="q-ma-sm"
                maxlength="38" />
              <q-input
                v-model="adult_info_sheet.adult.maternity_residence"
                outlined
                label="Res. "
                class="q-ma-sm"
                maxlength="38" />
              <q-input
                v-model="adult_info_sheet.adult.legal_guardian"
                outlined
                label="Tutore "
                class="q-ma-sm"
                maxlength="38" />

              <q-input
                v-model="adult_info_sheet.adult.legal_guardian_residence"
                outlined
                label="Res. "
                class="q-ma-sm"
                maxlength="20" />
              <q-input
                v-model="adult_info_sheet.adult.legal_guardian_phone_number"
                outlined
                label="Tel. "
                maxlength="15"
                type="tel"
                class="q-ma-sm" />
            </div>
            <div class="row">
              <q-input
                v-model="adult_info_sheet.adult.social_worker"
                outlined
                label="Assistente sociale "
                class="q-ma-sm"
                maxlength="27" />
              <q-input
                v-model="adult_info_sheet.adult.social_worker_municipality"
                outlined
                label="Comune di "
                class="q-ma-sm"
                maxlength="19" />
              <q-input
                v-model="adult_info_sheet.adult.social_worker_phone_number"
                outlined
                label="Tel. "
                maxlength="15"
                type="tel"
                class="q-ma-sm" />
            </div>
            <div class="row">
              <q-input
                v-model="adult_info_sheet.adult.amount_euro"
                outlined
                label="Importo Euro "
                type="number"
                class="q-ma-sm" />
              <q-input
                v-model="adult_info_sheet.adult.supplying_authority"
                outlined
                label="Ente erogatore "
                class="q-ma-sm"
                maxlength="50" />
              <q-input
                v-model="adult_info_sheet.adult.entry_date"
                outlined
                class="q-ma-sm"
                label="Data di ingresso "
                readonly>
                <template #append>
                  <q-icon name="event" class="cursor-pointer">
                    <q-popup-proxy
                      ref="qDateProxy"
                      cover
                      transition-show="scale"
                      transition-hide="scale">
                      <q-date
                        type="date"
                        :options="optionsFn"
                        @update:model-value="
                          (value, reason, detail) => {
                            watchDate(value, 'entry_date')
                          }
                        ">
                        <div class="row items-center justify-end">
                          <q-btn
                            v-close-popup
                            label="Close"
                            color="primary"
                            flat />
                        </div>
                      </q-date>
                    </q-popup-proxy>
                  </q-icon>
                </template>
              </q-input>
              <q-input
                v-model="adult_info_sheet.adult.entry_motivation"
                outlined
                label="Motivazione "
                class="q-ma-sm"
                style="flex-grow: 1"
                maxlength="62" />
            </div>

            <div class="row">
              <div class="col q-ma-sm">
                <q-input
                  v-model="adult_info_sheet.adult.disposal_date"
                  outlined
                  class="q-ma-sm"
                  label="Data di dismissione: "
                  readonly>
                  <template #append>
                    <q-icon name="event" class="cursor-pointer">
                      <q-popup-proxy
                        ref="qDateProxy"
                        cover
                        transition-show="scale"
                        transition-hide="scale">
                        <q-date
                          type="date"
                          :options="optionsFn"
                          @update:model-value="
                            (value, reason, detail) => {
                              watchDate(value, 'disposal_date')
                            }
                          ">
                          <div class="row items-center justify-end">
                            <q-btn
                              v-close-popup
                              label="Close"
                              color="primary"
                              flat />
                          </div>
                        </q-date>
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                </q-input>
              </div>
              <div class="col q-ma-sm">
                <q-input
                  v-model="adult_info_sheet.adult.disposal_motivation"
                  outlined
                  label="Motivazione "
                  maxlength="61"
                  class="q-ma-sm" />
              </div>
            </div>
            <div class="row">
              <div class="col">
                Portatore di handicap:
                <div class="row">
                  <div class="q-gutter-sm">
                    <q-radio
                      v-model="adult_info_sheet.adult.handicap.has_handicap"
                      :val="true"
                      label="SI" />
                    <q-radio
                      v-model="adult_info_sheet.adult.handicap.has_handicap"
                      :val="false"
                      label="No"
                      @click="reset('adult', 'handicap', 'type')" />
                  </div>
                  <q-select
                    v-if="adult_info_sheet.adult.handicap.has_handicap"
                    v-model="adult_info_sheet.adult.handicap.type"
                    outlined
                    :options="[
                      { label: 'Fisici', value: 'fisici' },
                      { label: 'Psichici', value: 'psichici' }
                    ]"
                    multiple
                    option-label="label"
                    option-value="value"
                    label="Tipo"
                    style="width: 30%"
                    class="q-mx-lg"
                    emit-value
                    map-options />
                </div>
              </div>
              <div class="col">
                Familiari presenti in struttura:
                <div class="row">
                  <div class="q-gutter-sm">
                    <q-radio
                      v-model="
                        adult_info_sheet.adult.family_member.in_structure
                      "
                      :val="true"
                      label="Si" />
                    <q-radio
                      v-model="
                        adult_info_sheet.adult.family_member.in_structure
                      "
                      :val="false"
                      label="No"
                      @click="reset('adult', 'family_member', 'member')" />
                  </div>
                  <q-select
                    v-if="adult_info_sheet.adult.family_member.in_structure"
                    v-model="adult_info_sheet.adult.family_member.member"
                    outlined
                    :options="[
                      { label: 'Madre', value: 'madre' },
                      { label: 'Sorella/e', value: 'sorella/e' },
                      { label: 'Fratello/i', value: 'fratello/i' }
                    ]"
                    multiple
                    option-label="label"
                    option-value="value"
                    label="Familiare"
                    style="width: 50%"
                    class="q-mx-lg"
                    emit-value
                    map-options />
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col">
                Proveniente da:
                <div class="row">
                  <q-select
                    v-model="adult_info_sheet.adult.origin.type"
                    outlined
                    :options="[
                      { label: 'Famiglia di origine', value: 'origin_family' },
                      { label: 'Famiglia affidataria', value: 'foster_family' },
                      { label: 'Famiglia Adottiva', value: 'adoptive_family' },
                      { label: 'Altro', value: 'other' },
                      {
                        label: 'Altra struttura specificare',
                        value: 'other_struct'
                      }
                    ]"
                    option-label="label"
                    option-value="value"
                    label="Tipologia"
                    style="width: 30%"
                    class="q-ma-sm"
                    emit-value
                    map-options
                    clearable
                    @clear="adult_info_sheet.adult.origin.type = ''"
                    @update:model-value="
                      adult_info_sheet.adult.origin.other = ''
                    " />
                  <q-input
                    v-if="adult_info_sheet.adult.origin.type === 'other'"
                    v-model="adult_info_sheet.adult.origin.other"
                    outlined
                    label="Altro "
                    class="q-ma-sm"
                    maxlength="52" />
                  <q-input
                    v-if="adult_info_sheet.adult.origin.type === 'other_struct'"
                    v-model="adult_info_sheet.adult.origin.detailed"
                    outlined
                    label="Altro "
                    class="q-ma-sm"
                    maxlength="54" />
                </div>
              </div>
              <div class="col">
                Collocati su disposizione di:
                <div class="row">
                  <q-select
                    v-model="adult_info_sheet.adult.placed_by.typology"
                    outlined
                    :options="[
                      { label: '(Ex art.403)', value: 'ex' },
                      { label: 'Genitori', value: 'parents' },
                      { label: 'Comune di :', value: 'mun' },
                      { label: 'Forze dell’ordine', value: 'police' }
                    ]"
                    multiple
                    option-label="label"
                    option-value="value"
                    label="Tipologia"
                    style="width: 30%"
                    class="q-ma-sm"
                    clearable
                    emit-value
                    map-options
                    @clear="adult_info_sheet.adult.placed_by.typology = []"
                    @update:model-value="
                      () => {
                        adult_info_sheet.adult.placed_by.type = ''
                        adult_info_sheet.adult.placed_by.pl_of = ''
                        adult_info_sheet.adult.placed_by.mun_of = ''
                        adult_info_sheet.adult.placed_by.tri_min_of = ''
                        adult_info_sheet.adult.placed_by.giudge = ''
                        adult_info_sheet.adult.placed_by.fasc_n = ''
                      }
                    " />
                  <q-select
                    v-if="
                      adult_info_sheet.adult.placed_by.typology.includes(
                        'police'
                      )
                    "
                    v-model="adult_info_sheet.adult.placed_by.type"
                    outlined
                    :options="[
                      { label: 'C.C.', value: 'cc' },
                      { label: 'P.S.', value: 'ps' },
                      { label: 'G.d.F.', value: 'gdf' },
                      { label: 'P.L. di ', value: 'pl' }
                    ]"
                    option-label="label"
                    option-value="value"
                    label="Tipo"
                    style="width: 30%"
                    class="q-ma-sm"
                    emit-value
                    map-options
                    @update:model-value="
                      adult_info_sheet.adult.placed_by.pl_of = ''
                    " />
                  <q-input
                    v-if="
                      adult_info_sheet.adult.placed_by.typology.includes(
                        'police'
                      ) && adult_info_sheet.adult.placed_by.type === 'pl'
                    "
                    v-model="adult_info_sheet.adult.placed_by.pl_of"
                    outlined
                    label=" "
                    style="width: 20%"
                    class="q-ma-sm"
                    maxlength="7" />
                  <q-input
                    v-if="
                      adult_info_sheet.adult.placed_by.typology.includes('mun')
                    "
                    v-model="adult_info_sheet.adult.placed_by.mun_of"
                    outlined
                    label="Comune di"
                    class="q-ma-sm"
                    maxlength="51" />
                </div>
              </div>
            </div>
            <div class="row">
              <q-input
                v-model="adult_info_sheet.adult.placed_by.tri_min_of"
                outlined
                label="Trib. Min. di "
                class="q-ma-sm q-mx-lg"
                maxlength="51" />
              <q-input
                v-model="adult_info_sheet.adult.placed_by.giudge"
                outlined
                label="Giudice: "
                class="q-ma-sm q-mx-lg"
                maxlength="33" />
              <q-input
                v-model="adult_info_sheet.adult.placed_by.fasc_n"
                outlined
                label="fasc.n° "
                class="q-ma-sm q-mx-lg"
                maxlength="15" />
            </div>
            <div class="row">
              <div class="col">
                Sospesa responsabilità genitoriale:
                <div class="row">
                  <q-radio
                    v-model="adult_info_sheet.adult.susp_parent_res"
                    :val="true"
                    label="SI"
                    class="q-ma-sm" />
                  <q-radio
                    v-model="adult_info_sheet.adult.susp_parent_res"
                    :val="false"
                    label="NO"
                    class="q-ma-sm" />
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col">
                Aspettative dell'Adulto:
                <div class="row">
                  <q-select
                    v-model="
                      adult_info_sheet.semestral_comunication.adult_expectation
                        .type
                    "
                    outlined
                    :options="[
                      { label: 'Rientri in Famiglia', value: 'family_returns' },
                      {
                        label: 'Percorsi di Autonomia',
                        value: 'autonomy_routes'
                      },
                      {
                        label: 'Affido Familiare',
                        value: 'family_foster_care'
                      },
                      { label: 'Non Valutabile', value: 'not_evaluable' },
                      { label: 'Adozione', value: 'adoption' },
                      { label: 'Altro', value: 'other' }
                    ]"
                    multiple
                    style="width: 30%"
                    option-label="label"
                    option-value="value"
                    label="Tipologia"
                    emit-value
                    map-options
                    @update:model-value="
                      !adult_info_sheet.semestral_comunication.adult_expectation.type.includes(
                        'other'
                      ) &&
                        (adult_info_sheet.semestral_comunication.adult_expectation.other =
                          '')
                    " />
                  <q-input
                    v-if="
                      adult_info_sheet.semestral_comunication.adult_expectation.type.includes(
                        'other'
                      )
                    "
                    v-model="
                      adult_info_sheet.semestral_comunication.adult_expectation
                        .other
                    "
                    outlined
                    label=" "
                    style="width: 30%"
                    class="q-mx-lg"
                    maxlength="47" />
                </div>
              </div>
              <div class="col">
                *Obiettivo:
                <div class="row">
                  <q-select
                    v-model="
                      adult_info_sheet.semestral_comunication.target.type
                    "
                    outlined
                    :options="[
                      { label: 'Rientri in Famiglia', value: 'family_returns' },
                      {
                        label: 'Percorsi di Autonomia',
                        value: 'autonomy_routes'
                      },
                      {
                        label: 'Affido Familiare',
                        value: 'family_foster_care'
                      },
                      { label: 'Non Valutabile', value: 'not_evaluable' },
                      { label: 'Adozione', value: 'adoption' },
                      { label: 'Altro', value: 'other' }
                    ]"
                    multiple
                    option-label="label"
                    option-value="value"
                    style="width: 30%"
                    label="Tipologia"
                    emit-value
                    map-options
                    @update:model-value="
                      adult_info_sheet.semestral_comunication.target.type.includes(
                        'other'
                      ) &&
                        (adult_info_sheet.semestral_comunication.target.other =
                          '')
                    " />
                  <q-input
                    v-if="
                      adult_info_sheet.semestral_comunication.target.type.includes(
                        'other'
                      )
                    "
                    v-model="
                      adult_info_sheet.semestral_comunication.target.other
                    "
                    outlined
                    label="  "
                    style="width: 30%"
                    class="q-mx-lg"
                    maxlength="86" />
                </div>
              </div>
            </div>
            <div class="column q-mt-md q-mb-xl">
              Data scheda:
              <q-date
                v-model="adult_info_sheet.semestral_comunication.date"
                :locale="locale"
                mask="DD/MM/YYYY"
                format="DD/MM/YYYY" />
            </div>

            <div class="row">
              <q-btn label="Salva informazioni" type="submit" color="primary" />
            </div>
          </q-form></div
      ></q-card>
    </div>
  </q-page>
</template>

<script>
import Heading from 'components/Heading.vue'
import { useQuasar } from 'quasar'
import moment from 'moment'
import { api } from 'src/boot/axios'
import { date } from 'quasar'

export default {
  name: 'AdultInfoSheet',
  components: {
    Heading
  },
  props: {
    id: {
      type: String,
      required: false,
      default: ''
    },
    isFirstPriceEdit: {
      type: Boolean,
      required: false,
      default: false
    }
  },
  setup() {
    const $q = useQuasar()

    return {
      optionsFn(d) {
        return d <= date.formatDate(Date.now(), 'YYYY/MM/DD')
      },
      showNotif(tp, msg) {
        $q.notify({
          type: tp,
          message: msg,
          position: 'top-right',
          timeout: 2000
        })
      }
    }
  },
  data() {
    return {
      locale: {
        days: 'Domenica_Lunedì_Martedì_Mercoledì_Giovedì_Venerdì_Sabato'.split(
          '_'
        ),
        daysShort: 'Dom_Lun_Mar_Mer_Gio_Ven_Sab'.split('_'),
        months:
          'Gennaio_Febbraio_Marzo_Aprile_Maggio_Giugno_Luglio_Agosto_Settembre_Ottobre_Novembre_Dicembre'.split(
            '_'
          ),
        monthsShort: 'Gen_Feb_Mar_Apr_Mag_Giu_Lug_Ago_Set_Ott_Nov_Dic'.split(
          '_'
        ),
        firstDayOfWeek: 1
      },
      adult_info_sheet: {
        community: {
          name: '',
          address: '',
          county: '',
          municipality: '',
          phone_number: ''
        },
        adult: {
          name: '',
          surname: '',
          birthdate: '',
          birthplace: '',
          resident: '',
          county: '',
          paternity: '',
          paternity_residence: '',
          maternity: '',
          maternity_residence: '',
          legal_guardian: '',
          legal_guardian_residence: '',
          legal_guardian_phone_number: '',
          social_worker: '',
          social_worker_municipality: '',
          social_worker_phone_number: '',
          amount_euro: '',
          supplying_authority: '',
          entry_date: '',
          entry_motivation: '',
          conditions: '',
          disposal_date: '',
          disposal_motivation: '',
          handicap: {
            has_handicap: false,
            type: []
          },
          family_member: {
            in_structure: false,
            member: []
          },
          origin: {
            type: '',
            other: '',
            detailed: ''
          },
          placed_by: {
            typology: [],
            mun_of: '',
            type: '',
            pl_of: '',
            tri_min_of: '',
            giudge: '',
            fasc_n: ''
          },
          susp_parent_res: false
        },
        semestral_comunication: {
          adult_expectation: {
            type: [],
            other: ''
          },
          target: {
            type: [],
            other: ''
          },
          date: ''
        }
      },
      isFirstPriceEditBool: this.isFirstPriceEdit === 'true'
    }
  },
  mounted() {
    if (this.id) {
      this.getAdult(this.id)
    }
  },
  methods: {
    reset(category, fieldObject, field) {
      this.adult_info_sheet[category][fieldObject][field] = []
    },
    getAdult(id) {
      api.get('/adults/adult/' + id).then(response => {
        if (response.data?.info_sheet) {
          this.adult_info_sheet = response.data['info_sheet']
          this.adult_info_sheet.adult.name = response.data.name
          this.adult_info_sheet.adult.surname = response.data.surname
        } else {
          this.adult_info_sheet.adult.name = response.data.name
          this.adult_info_sheet.adult.surname = response.data.surname
        }
      })
    },
    dataURItoBlob(dataURI) {
      const byteString = window.atob(dataURI)
      const arrayBuffer = new ArrayBuffer(byteString.length)
      const int8Array = new Uint8Array(arrayBuffer)
      for (let i = 0; i < byteString.length; i++) {
        int8Array[i] = byteString.charCodeAt(i)
      }
      const blob = new Blob([int8Array], { type: 'application/pdf' })
      return blob
    },
    validate(info_sheet) {
      let isValid = true
      if (
        info_sheet.adult.birthdate !== '' &&
        info_sheet.adult.entry_date !== ''
      ) {
        if (
          moment(info_sheet.adult.birthdate, 'DD/MM/YYYY').isAfter(
            moment(info_sheet.adult.entry_date, 'DD/MM/YYYY')
          )
        ) {
          this.showNotif(
            'warning',
            "Attenzione! La data di ingresso non può essere precedente alla data di nascita dell'adulto"
          )
          info_sheet.adult.entry_date = ''
          isValid = false
        }
      }

      if (
        info_sheet.adult.entry_date !== '' &&
        info_sheet.adult.disposal_date !== ''
      ) {
        if (
          moment(info_sheet.adult.entry_date, 'DD/MM/YYYY').isAfter(
            moment(info_sheet.adult.disposal_date, 'DD/MM/YYYY')
          )
        ) {
          this.showNotif(
            'warning',
            'Attenzione! La data di uscita non può essere precedente alla data di ingresso'
          )
          info_sheet.adult.disposal_date = ''
          isValid = false
        }
      }
      if (
        info_sheet.adult.birthdate !== '' &&
        info_sheet.adult.disposal_date !== ''
      ) {
        if (
          moment(info_sheet.adult.birthdate, 'DD/MM/YYYY').isAfter(
            moment(info_sheet.adult.disposal_date, 'DD/MM/YYYY')
          )
        ) {
          this.showNotif(
            'warning',
            "Attenzione! La data di uscita non può essere precedente alla data di nascita dell'adulto"
          )
          info_sheet.adult.disposal_date = ''
          isValid = false
        }
      }
      if (info_sheet.adult.disposal_date !== '') {
        if (info_sheet.adult.entry_date === '') {
          this.showNotif(
            'warning',
            'Attenzione! La data di ingresso non può essere vuota se è presente la data di uscita'
          )
          isValid = false
        }
      }
      if (info_sheet.adult.entry_date !== '') {
        if (
          info_sheet.adult.amount_euro === '' ||
          isNaN(info_sheet.adult.amount_euro.replace(',', '.'))
        ) {
          this.showNotif(
            'warning',
            "Attenzione! L'importo non può essere vuoto se è presente la data di ingresso"
          )
          isValid = false
        }
      }
      if (
        info_sheet.adult.birthdate !== '' &&
        info_sheet.adult.disposal_date !== ''
      ) {
        if (
          moment(info_sheet.adult.birthdate, 'DD/MM/YYYY').isAfter(
            moment(info_sheet.adult.disposal_date, 'DD/MM/YYYY')
          )
        ) {
          this.showNotif(
            'warning',
            "Attenzione! La data di uscita non può essere precedente alla data di nascita dell'adulto"
          )
          info_sheet.adult.disposal_date = ''
          isValid = false
        }
      }
      if (info_sheet.adult.disposal_date !== '') {
        if (info_sheet.adult.entry_date === '') {
          this.showNotif(
            'warning',
            'Attenzione! La data di ingresso non può essere vuota se è presente la data di uscita'
          )
          isValid = false
        }
      }
      if (info_sheet.adult.entry_date !== '') {
        if (
          info_sheet.adult.amount_euro === '' ||
          isNaN(info_sheet.adult.amount_euro.replace(',', '.'))
        ) {
          this.showNotif(
            'warning',
            "Attenzione! L'importo non può essere vuoto se è presente la data di ingresso"
          )
          isValid = false
        }
      }
      return isValid
    },
    onSubmit() {
      if (this.id && this.validate(this.adult_info_sheet)) {
        api
          .post('/adults/adult/' + this.id, this.adult_info_sheet)
          .then(() => {
            if (
              this.isFirstPriceEditBool &&
              !!parseFloat(this.adult_info_sheet.adult.amount_euro) &&
              !!this.adult_info_sheet.adult.entry_date
            ) {
              this.addTariff(
                this.id,
                parseFloat(this.adult_info_sheet.adult.amount_euro),
                this.adult_info_sheet.adult.entry_date
                  .split('/')
                  .reverse()
                  .join('-')
              )
            } else {
              this.$router.push('/adults')
              this.showNotif(
                'positive',
                "Scheda informativa dell'adulto modificata con successo."
              )
            }
          })
          .catch(() => {
            this.showNotif(
              'warning',
              "Errore durante la modifica della scheda informativa dell'adulto."
            )
          })
      }
    },
    addTariff(adultId, value, timestamp) {
      api
        .post('/adults/adult/' + adultId + '/price', {
          value: value,
          timestamp: timestamp
        })
        .then(() => {
          this.$router.push('/adults')
          this.showNotif(
            'positive',
            "Scheda informativa dell'adulto modificata con successo."
          )
        })
        .catch(() => {
          this.showNotif(
            'warning',
            "Non è stato possibile creare la tariffa per l'adulto."
          )
        })
    },
    watchDate(value, field) {
      this.adult_info_sheet.adult[field] = moment(value).format('DD/MM/YYYY')
    }
  }
}
</script>
<style scoped></style>
