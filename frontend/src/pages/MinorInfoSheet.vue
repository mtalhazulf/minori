<template>
  <q-page class="q-mx-xl">
    <div class="row"><Heading :title="'Scheda informativa minore'" /></div>
    <div class="row">
      <q-card style="width: 100%"
        ><div class="q-pa-md">
          <q-form class="q-gutter-md col" @submit="onSubmit">
            <div class="row text-center justify-center">INFO COMUNITA'</div>
            <div class="row">
              <q-input
                v-model="minor_info_sheet.community.name"
                outlined
                label="Comunità "
                class="q-ma-sm"
                maxlength="58" />
              <q-input
                v-model="minor_info_sheet.community.address"
                outlined
                label="Via "
                class="q-ma-sm"
                maxlength="33" />
              <q-input
                v-model="minor_info_sheet.community.county"
                outlined
                label="Prov. "
                class="q-ma-sm"
                maxlength="19" />
              <q-input
                v-model="minor_info_sheet.community.municipality"
                outlined
                label="Comune "
                class="q-ma-sm"
                maxlength="33" />
              <q-input
                v-model="minor_info_sheet.community.phone_number"
                outlined
                label="Tel. "
                maxlength="15"
                type="tel"
                class="q-ma-sm" />
            </div>
            <div class="row text-center justify-center">INFO OSPITE</div>
            <div class="row">
              <q-input
                v-model="minor_info_sheet.minor.surname"
                outlined
                label="Cognome "
                class="q-ma-sm"
                maxlength="26"
                :disable="true" />
              <q-input
                v-model="minor_info_sheet.minor.name"
                outlined
                label="Nome "
                class="q-ma-sm"
                maxlength="26"
                :disable="true" />
              <q-input
                v-model="minor_info_sheet.minor.birthdate"
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
                v-model="minor_info_sheet.minor.birthplace"
                outlined
                label="a "
                class="q-ma-sm"
                maxlength="29" />
            </div>
            <div class="row">
              <q-input
                v-model="minor_info_sheet.minor.resident"
                outlined
                label="Residente "
                class="q-ma-sm"
                maxlength="42" />
              <q-input
                v-model="minor_info_sheet.minor.county"
                outlined
                label="Prov. "
                class="q-ma-sm"
                maxlength="15" />
              <q-input
                v-model="minor_info_sheet.minor.paternity"
                outlined
                label="Paternità "
                class="q-ma-sm"
                maxlength="38" />
              <q-input
                v-model="minor_info_sheet.minor.paternity_residence"
                outlined
                label="Res. "
                class="q-ma-sm"
                maxlength="38" />
            </div>
            <div class="row">
              <q-input
                v-model="minor_info_sheet.minor.maternity"
                outlined
                label="Maternità "
                class="q-ma-sm"
                maxlength="38" />
              <q-input
                v-model="minor_info_sheet.minor.maternity_residence"
                outlined
                label="Res. "
                class="q-ma-sm"
                maxlength="38" />
              <q-input
                v-model="minor_info_sheet.minor.legal_guardian"
                outlined
                label="Tutore "
                class="q-ma-sm"
                maxlength="38" />

              <q-input
                v-model="minor_info_sheet.minor.legal_guardian_residence"
                outlined
                label="Res. "
                class="q-ma-sm"
                maxlength="20" />
              <q-input
                v-model="minor_info_sheet.minor.legal_guardian_phone_number"
                outlined
                label="Tel. "
                maxlength="15"
                type="tel"
                class="q-ma-sm" />
            </div>
            <div class="row">
              <q-input
                v-model="minor_info_sheet.minor.social_worker"
                outlined
                label="Assistente sociale "
                class="q-ma-sm"
                maxlength="27" />
              <q-input
                v-model="minor_info_sheet.minor.social_worker_municipality"
                outlined
                label="Comune di "
                class="q-ma-sm"
                maxlength="19" />
              <q-input
                v-model="minor_info_sheet.minor.social_worker_phone_number"
                outlined
                label="Tel. "
                maxlength="15"
                type="tel"
                class="q-ma-sm" />
            </div>
            <div class="row">
              <q-input
                v-model="minor_info_sheet.minor.amount_euro"
                outlined
                label="Importo Euro "
                type="number"
                class="q-ma-sm" />
              <q-input
                v-model="minor_info_sheet.minor.supplying_authority"
                outlined
                label="Ente erogatore "
                class="q-ma-sm"
                maxlength="50" />
              <q-input
                v-model="minor_info_sheet.minor.entry_date"
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
                v-model="minor_info_sheet.minor.entry_motivation"
                outlined
                label="Motivazione "
                class="q-ma-sm"
                style="flex-grow: 1"
                maxlength="62" />
            </div>
            <div class="row">
              <q-input
                v-model="minor_info_sheet.minor.conditions"
                outlined
                type="textarea"
                class="q-ma-sm"
                style="width: 100%"
                label="Condizioni fisiche e psichiche del minore all’ingresso:"
                maxlength="171" />
            </div>
            <div class="row">
              <div class="col q-ma-sm">
                <q-input
                  v-model="minor_info_sheet.minor.disposal_date"
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
                  v-model="minor_info_sheet.minor.disposal_motivation"
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
                      v-model="minor_info_sheet.minor.handicap.has_handicap"
                      :val="true"
                      label="SI" />
                    <q-radio
                      v-model="minor_info_sheet.minor.handicap.has_handicap"
                      :val="false"
                      label="No"
                      @click="reset('minor', 'handicap', 'type')" />
                  </div>
                  <q-select
                    v-if="minor_info_sheet.minor.handicap.has_handicap"
                    v-model="minor_info_sheet.minor.handicap.type"
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
                        minor_info_sheet.minor.family_member.in_structure
                      "
                      :val="true"
                      label="Si" />
                    <q-radio
                      v-model="
                        minor_info_sheet.minor.family_member.in_structure
                      "
                      :val="false"
                      label="No"
                      @click="reset('minor', 'family_member', 'member')" />
                  </div>
                  <q-select
                    v-if="minor_info_sheet.minor.family_member.in_structure"
                    v-model="minor_info_sheet.minor.family_member.member"
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
                    v-model="minor_info_sheet.minor.origin.type"
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
                    @clear="minor_info_sheet.minor.origin.type = ''"
                    @update:model-value="
                      minor_info_sheet.minor.origin.other = ''
                    " />
                  <q-input
                    v-if="minor_info_sheet.minor.origin.type === 'other'"
                    v-model="minor_info_sheet.minor.origin.other"
                    outlined
                    label="Altro "
                    class="q-ma-sm"
                    maxlength="52" />
                  <q-input
                    v-if="minor_info_sheet.minor.origin.type === 'other_struct'"
                    v-model="minor_info_sheet.minor.origin.detailed"
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
                    v-model="minor_info_sheet.minor.placed_by.typology"
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
                    emit-value
                    map-options
                    clearable
                    @clear="minor_info_sheet.minor.placed_by.typology = []"
                    @update:model-value="
                      () => {
                        minor_info_sheet.minor.placed_by.type = ''
                        minor_info_sheet.minor.placed_by.pl_of = ''
                        minor_info_sheet.minor.placed_by.mun_of = ''
                        minor_info_sheet.minor.placed_by.tri_min_of = ''
                        minor_info_sheet.minor.placed_by.giudge = ''
                        minor_info_sheet.minor.placed_by.fasc_n = ''
                      }
                    " />
                  <q-select
                    v-if="
                      minor_info_sheet.minor.placed_by.typology.includes(
                        'police'
                      )
                    "
                    v-model="minor_info_sheet.minor.placed_by.type"
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
                      minor_info_sheet.minor.placed_by.pl_of = ''
                    " />
                  <q-input
                    v-if="
                      minor_info_sheet.minor.placed_by.typology.includes(
                        'police'
                      ) && minor_info_sheet.minor.placed_by.type === 'pl'
                    "
                    v-model="minor_info_sheet.minor.placed_by.pl_of"
                    outlined
                    label=" "
                    style="width: 20%"
                    class="q-ma-sm"
                    maxlength="7" />
                  <q-input
                    v-if="
                      minor_info_sheet.minor.placed_by.typology.includes('mun')
                    "
                    v-model="minor_info_sheet.minor.placed_by.mun_of"
                    outlined
                    label="Comune di"
                    class="q-ma-sm"
                    maxlength="51" />
                </div>
              </div>
            </div>
            <div class="row">
              <q-input
                v-model="minor_info_sheet.minor.placed_by.tri_min_of"
                outlined
                label="Trib. Min. di "
                class="q-ma-sm q-mx-lg"
                maxlength="51" />
              <q-input
                v-model="minor_info_sheet.minor.placed_by.giudge"
                outlined
                label="Giudice: "
                class="q-ma-sm q-mx-lg"
                maxlength="33" />
              <q-input
                v-model="minor_info_sheet.minor.placed_by.fasc_n"
                outlined
                label="fasc.n° "
                class="q-ma-sm q-mx-lg"
                maxlength="15" />
            </div>
            <div class="row text-center justify-center">
              PARTE RISERVATA ALLA COMUNICAZIONE SEMESTRALE
            </div>

            <div class="row">
              Incontri con i familiari:
              <div class="q-gutter-sm">
                <q-select
                  v-model="
                    minor_info_sheet.semestral_comunication
                      .family_members_meeting.member
                  "
                  outlined
                  multiple
                  :options="[
                    { label: 'padre', value: 'padre' },
                    { label: 'madre', value: 'madre' },
                    { label: 'fratelli', value: 'fratelli' },
                    { label: 'nonni', value: 'nonni' },
                    { label: 'zii', value: 'zii' }
                  ]"
                  option-label="label"
                  option-value="value"
                  label="Membri della famiglia"
                  style="width: 100%"
                  class="q-ma-sm q-ml-lg"
                  emit-value
                  map-options />
              </div>
            </div>
            <div class="row">
              <div class="col">
                <div class="row">In Comunità:</div>
                <div class="row">Rientri in famiglia:</div>
              </div>
              <div class="col">
                <div class="row">
                  <div class="q-gutter-sm q-mx-sm">
                    <q-radio
                      v-model="
                        minor_info_sheet.semestral_comunication
                          .family_members_meeting.in_community
                      "
                      :val="true"
                      label="Si" />
                    <q-radio
                      v-model="
                        minor_info_sheet.semestral_comunication
                          .family_members_meeting.in_community
                      "
                      :val="false"
                      label="No"
                      @click="
                        () => {
                          minor_info_sheet.semestral_comunication.family_members_meeting.in_community_freq =
                            ''
                          minor_info_sheet.semestral_comunication.family_members_meeting.in_community_duration =
                            ''
                        }
                      " />
                  </div>
                </div>
                <div class="row">
                  <div class="q-gutter-sm q-mx-sm">
                    <q-radio
                      v-model="
                        minor_info_sheet.semestral_comunication
                          .family_members_meeting.return_to_family
                      "
                      :val="true"
                      label="Si" />
                    <q-radio
                      v-model="
                        minor_info_sheet.semestral_comunication
                          .family_members_meeting.return_to_family
                      "
                      :val="false"
                      label="No"
                      @click="
                        () => {
                          minor_info_sheet.semestral_comunication.family_members_meeting.return_to_family_freq =
                            ''
                          minor_info_sheet.semestral_comunication.family_members_meeting.return_to_family_duration =
                            ''
                        }
                      " />
                  </div>
                </div>
              </div>
              <div class="col">
                <div class="row">
                  <q-input
                    v-if="
                      minor_info_sheet.semestral_comunication
                        .family_members_meeting.in_community
                    "
                    v-model="
                      minor_info_sheet.semestral_comunication
                        .family_members_meeting.in_community_freq
                    "
                    outlined
                    label="frequenza "
                    class="q-mx-lg"
                    maxlength="23" />
                </div>
                <div class="row">
                  <q-input
                    v-if="
                      minor_info_sheet.semestral_comunication
                        .family_members_meeting.return_to_family
                    "
                    v-model="
                      minor_info_sheet.semestral_comunication
                        .family_members_meeting.return_to_family_freq
                    "
                    outlined
                    label="frequenza "
                    class="q-mx-lg"
                    maxlength="23" />
                </div>
              </div>
              <div class="col">
                <div class="row">
                  <q-input
                    v-if="
                      minor_info_sheet.semestral_comunication
                        .family_members_meeting.in_community
                    "
                    v-model="
                      minor_info_sheet.semestral_comunication
                        .family_members_meeting.in_community_duration
                    "
                    outlined
                    label="durata "
                    class="q-mx-lg"
                    maxlength="28" />
                </div>
                <div class="row">
                  <q-input
                    v-if="
                      minor_info_sheet.semestral_comunication
                        .family_members_meeting.return_to_family
                    "
                    v-model="
                      minor_info_sheet.semestral_comunication
                        .family_members_meeting.return_to_family_duration
                    "
                    outlined
                    label="durata "
                    class="q-mx-lg"
                    maxlength="28" />
                </div>
              </div>
            </div>
            <div class="row">
              Incontri con: famiglie indicate da
              <div class="q-gutter-sm q-mx-lg">
                <q-radio
                  v-model="
                    minor_info_sheet.semestral_comunication
                      .family_members_meeting_by.name
                  "
                  val="social_service"
                  label="Serv. sociale" />
                <q-radio
                  v-model="
                    minor_info_sheet.semestral_comunication
                      .family_members_meeting_by.name
                  "
                  val="community_resp"
                  label="Resp. Comunità" />
                <q-radio
                  v-model="
                    minor_info_sheet.semestral_comunication
                      .family_members_meeting_by.name
                  "
                  val="tm"
                  label="T.M." />
                <q-radio
                  v-model="
                    minor_info_sheet.semestral_comunication
                      .family_members_meeting_by.name
                  "
                  val="volunteers_family"
                  label="Famiglie di volontari" />
              </div>
            </div>
            <div class="row">
              <div class="col">
                <div class="row">In Comunità:</div>
                <div class="row">Presso il domicilio:</div>
              </div>
              <div class="col">
                <div class="row">
                  <div class="q-gutter-sm q-mx-sm">
                    <q-radio
                      v-model="
                        minor_info_sheet.semestral_comunication
                          .family_members_meeting_by.in_community
                      "
                      :val="true"
                      label="Si" />
                    <q-radio
                      v-model="
                        minor_info_sheet.semestral_comunication
                          .family_members_meeting_by.in_community
                      "
                      :val="false"
                      label="No"
                      @click="
                        () => {
                          minor_info_sheet.semestral_comunication.family_members_meeting_by.in_community_freq =
                            ''
                          minor_info_sheet.semestral_comunication.family_members_meeting_by.in_community_duration =
                            ''
                        }
                      " />
                  </div>
                </div>
                <div class="row">
                  <div class="q-gutter-sm q-mx-sm">
                    <q-radio
                      v-model="
                        minor_info_sheet.semestral_comunication
                          .family_members_meeting_by.return_home
                      "
                      :val="true"
                      label="Si" />
                    <q-radio
                      v-model="
                        minor_info_sheet.semestral_comunication
                          .family_members_meeting_by.return_home
                      "
                      :val="false"
                      label="No"
                      @click="
                        () => {
                          minor_info_sheet.semestral_comunication.family_members_meeting_by.return_home_freq =
                            ''
                          minor_info_sheet.semestral_comunication.family_members_meeting.return_home__duration =
                            ''
                        }
                      " />
                  </div>
                </div>
              </div>
              <div class="col">
                <div class="row">
                  <q-input
                    v-if="
                      minor_info_sheet.semestral_comunication
                        .family_members_meeting_by.in_community
                    "
                    v-model="
                      minor_info_sheet.semestral_comunication
                        .family_members_meeting_by.in_community_freq
                    "
                    outlined
                    label="frequenza "
                    class="q-mx-lg"
                    maxlength="23" />
                </div>
                <div class="row">
                  <q-input
                    v-if="
                      minor_info_sheet.semestral_comunication
                        .family_members_meeting_by.return_home
                    "
                    v-model="
                      minor_info_sheet.semestral_comunication
                        .family_members_meeting_by.return_home_freq
                    "
                    outlined
                    label="frequenza "
                    class="q-mx-lg"
                    maxlength="23" />
                </div>
              </div>
              <div class="col">
                <div class="row">
                  <q-input
                    v-if="
                      minor_info_sheet.semestral_comunication
                        .family_members_meeting_by.in_community
                    "
                    v-model="
                      minor_info_sheet.semestral_comunication
                        .family_members_meeting_by.in_community_duration
                    "
                    outlined
                    label="durata "
                    class="q-mx-lg"
                    maxlength="28" />
                </div>
                <div class="row">
                  <q-input
                    v-if="
                      minor_info_sheet.semestral_comunication
                        .family_members_meeting_by.return_home
                    "
                    v-model="
                      minor_info_sheet.semestral_comunication
                        .family_members_meeting_by.return_home_duration
                    "
                    outlined
                    label="durata "
                    class="q-mx-lg"
                    maxlength="28" />
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col">
                Visite del tutore:
                <div class="row">
                  <div class="q-gutter-sm q-mr-lg">
                    <q-radio
                      v-model="
                        minor_info_sheet.semestral_comunication
                          .legal_guardian_visit
                      "
                      :val="true"
                      label="Si" />
                    <q-radio
                      v-model="
                        minor_info_sheet.semestral_comunication
                          .legal_guardian_visit
                      "
                      :val="false"
                      label="No"
                      @click="
                        minor_info_sheet.semestral_comunication.legal_guardian_visit_freq =
                          ''
                      " />
                  </div>
                  <q-input
                    v-if="
                      minor_info_sheet.semestral_comunication
                        .legal_guardian_visit
                    "
                    v-model="
                      minor_info_sheet.semestral_comunication
                        .legal_guardian_visit_freq
                    "
                    outlined
                    label="frequenza "
                    style="width: 30%"
                    class="q-mx-lg"
                    maxlength="12" />
                </div>
              </div>
              <div class="col">
                Visite dell’ass. soc.:
                <div class="row">
                  <div class="q-gutter-sm q-mr-lg">
                    <q-radio
                      v-model="
                        minor_info_sheet.semestral_comunication.ass_soc_visit
                      "
                      :val="true"
                      label="Si" />
                    <q-radio
                      v-model="
                        minor_info_sheet.semestral_comunication.ass_soc_visit
                      "
                      :val="false"
                      label="No"
                      @click="
                        minor_info_sheet.semestral_comunication.ass_soc_visit_freq =
                          ''
                      " />
                  </div>
                  <q-input
                    v-if="minor_info_sheet.semestral_comunication.ass_soc_visit"
                    v-model="
                      minor_info_sheet.semestral_comunication.ass_soc_visit_freq
                    "
                    outlined
                    label="frequenza "
                    style="width: 30%"
                    class="q-mx-lg"
                    maxlength="12" />
                </div>
              </div>
            </div>

            <!-- Summarize button -->
            <!-- <div class="row">
              <q-btn label="Valutazione dell'intelligenza artificiale" color="primary" 
                @click="
                  generate_summary()
              "
              :loading="isSummaryLoading"/>
            </div> -->

            <div class="row justify-between">
              <q-btn
                label="Valutazione dell'intelligenza artificiale"
                color="primary"
                :loading="isSummaryLoading"
                @click="generate_summary" />

              <!-- New Dropdown for selecting period -->
              <div>
                <label>Start Date</label>
                <q-btn color="grey" class="q-ml-md">
                  {{ startDate }}
                  <q-icon name="event" class="q-ml-md" />
                  <q-popup-proxy ref="qDateProxy">
                    <q-date
                      v-model="startDate"
                      mask="DD/MM/YYYY"
                      :format24h="true"
                      :locale="itLocale"
                      :options="isDateBeforeToday"
                      no-unset
                      @update:model-value="
                        () => {
                          $refs.qDateProxy.hide()
                        }
                      " />
                  </q-popup-proxy>
                </q-btn>

                <label class="q-ml-md">End Date</label>
                <q-btn color="grey" class="q-ml-md">
                  {{ endDate }}
                  <q-icon name="event" class="q-ml-md" />
                  <q-popup-proxy ref="qDateProxy">
                    <q-date
                      v-model="endDate"
                      mask="DD/MM/YYYY"
                      :format24h="true"
                      :locale="itLocale"
                      :options="isDateBeforeToday"
                      no-unset
                      @update:model-value="
                        () => {
                          $refs.qDateProxy.hide()
                        }
                      " />
                  </q-popup-proxy>
                </q-btn>
              </div>
            </div>

            <div class="row">
              <q-input
                v-model="minor_info_sheet.semestral_comunication.ai_report"
                :disable="isSummaryLoading"
                outlined
                type="textarea"
                label="Rapporto dell'AI:"
                class="q-ma-sm"
                style="width: 100%" />
            </div>
            <div class="row">
              <q-input
                v-model="
                  minor_info_sheet.semestral_comunication.evolutionary_path
                "
                outlined
                type="textarea"
                label="Percorso evolutivo:"
                class="q-ma-sm"
                style="width: 100%"
                maxlength="200" />
            </div>
            <div class="row">
              <q-input
                v-model="
                  minor_info_sheet.semestral_comunication
                    .added_section_evolutionary_path
                "
                outlined
                type="textarea"
                label="Sezione aggiuntiva percorso evolutivo:"
                class="q-ma-sm"
                style="width: 100%"
                maxlength="1775" />
            </div>
            <div class="row">
              <div class="col">
                Aspettattive del Minore:
                <div class="row">
                  <q-select
                    v-model="
                      minor_info_sheet.semestral_comunication.minor_expectation
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
                      !minor_info_sheet.semestral_comunication.minor_expectation.type.includes(
                        'other'
                      ) &&
                        (minor_info_sheet.semestral_comunication.minor_expectation.other =
                          '')
                    " />
                  <q-input
                    v-if="
                      minor_info_sheet.semestral_comunication.minor_expectation.type.includes(
                        'other'
                      )
                    "
                    v-model="
                      minor_info_sheet.semestral_comunication.minor_expectation
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
                      minor_info_sheet.semestral_comunication.target.type
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
                      !minor_info_sheet.semestral_comunication.target.type.includes(
                        'other'
                      ) &&
                        (minor_info_sheet.semestral_comunication.target.other =
                          '')
                    " />
                  <q-input
                    v-if="
                      minor_info_sheet.semestral_comunication.target.type.includes(
                        'other'
                      )
                    "
                    v-model="
                      minor_info_sheet.semestral_comunication.target.other
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
                v-model="minor_info_sheet.semestral_comunication.date"
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
  name: 'MinorInfoSheet',
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
      isSummaryLoading: false,
      isPeriodDropdownDisabled: false,
      startDate: {},
      endDate: {},
      today: new Date().toLocaleDateString('it-IT', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      }),
      convertDateForBackend(date) {
        //convert MM/DD/YYYY to YYYY-MM-DD
        return date.split('/').reverse().join('-')
      },

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
      minor_info_sheet: {
        community: {
          name: '',
          address: '',
          county: '',
          municipality: '',
          phone_number: ''
        },
        minor: {
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
          }
        },
        semestral_comunication: {
          ai_report: '',
          family_members_meeting: {
            member: [],
            in_community: false,
            in_community_freq: '',
            in_community_duration: '',
            return_to_family: false,
            return_to_family_freq: '',
            return_to_family_duration: ''
          },
          family_members_meeting_by: {
            name: '',
            in_community: false,
            in_community_freq: '',
            in_community_duration: '',
            return_home: false,
            return_home_freq: '',
            return_home_duration: ''
          },
          legal_guardian_visit: false,
          legal_guardian_visit_freq: '',
          ass_soc_visit: false,
          ass_soc_visit_freq: '',
          evolutionary_path: '',
          added_section_evolutionary_path: '',
          minor_expectation: {
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
      this.getMinor(this.id)
    }
    this.startDate = this.today
    this.endDate = this.today
  },
  methods: {
    reset(category, fieldObject, field) {
      this.minor_info_sheet[category][fieldObject][field] = []
    },
    getMinor(id) {
      api.get('/minors/minor/' + id).then(response => {
        if (response.data?.info_sheet) {
          this.minor_info_sheet = response.data['info_sheet']
          this.minor_info_sheet.minor.name = response.data.name
          this.minor_info_sheet.minor.surname = response.data.surname
        } else {
          this.minor_info_sheet.minor.name = response.data.name
          this.minor_info_sheet.minor.surname = response.data.surname
        }
      })
    },

    // Generate Summary
    generate_summary() {
      this.isSummaryLoading = true
      api
        .post('/minors/generate_summary', {
          id: this.id,
          info_sheet: this.minor_info_sheet,
          start_date: this.convertDateForBackend(this.startDate),
          end_date: this.convertDateForBackend(this.endDate)
        })
        .then(response => {
          this.isSummaryLoading = false
          this.minor_info_sheet.semestral_comunication.ai_report =
            response.data.summary
          this.$forceUpdate()
        })
        .catch(error => {
          console.error('Error Generating Summary:', error)
        })
    },

    selectPeriod(option) {
      this.selectedPeriod = option.value
      this.selectedPeriodLabel = option.label
      // this.handlePeriodSelection(option.value);
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
        info_sheet.minor.birthdate !== '' &&
        info_sheet.minor.entry_date !== ''
      ) {
        if (
          moment(info_sheet.minor.birthdate, 'DD/MM/YYYY').isAfter(
            moment(info_sheet.minor.entry_date, 'DD/MM/YYYY')
          )
        ) {
          this.showNotif(
            'warning',
            'Attenzione! La data di ingresso non può essere precedente alla data di nascita del minore'
          )
          info_sheet.minor.entry_date = ''
          isValid = false
        }
      }

      if (
        info_sheet.minor.entry_date !== '' &&
        info_sheet.minor.disposal_date !== ''
      ) {
        if (
          moment(info_sheet.minor.entry_date, 'DD/MM/YYYY').isAfter(
            moment(info_sheet.minor.disposal_date, 'DD/MM/YYYY')
          )
        ) {
          this.showNotif(
            'warning',
            'Attenzione! La data di uscita non può essere precedente alla data di ingresso'
          )
          info_sheet.minor.disposal_date = ''
          isValid = false
        }
      }
      if (
        info_sheet.minor.birthdate !== '' &&
        info_sheet.minor.disposal_date !== ''
      ) {
        if (
          moment(info_sheet.minor.birthdate, 'DD/MM/YYYY').isAfter(
            moment(info_sheet.minor.disposal_date, 'DD/MM/YYYY')
          )
        ) {
          this.showNotif(
            'warning',
            'Attenzione! La data di uscita non può essere precedente alla data di nascita del minore'
          )
          info_sheet.minor.disposal_date = ''
          isValid = false
        }
      }
      if (info_sheet.minor.disposal_date !== '') {
        if (info_sheet.minor.entry_date === '') {
          this.showNotif(
            'warning',
            'Attenzione! La data di ingresso non può essere vuota se è presente la data di uscita'
          )
          isValid = false
        }
      }
      if (info_sheet.minor.entry_date !== '') {
        if (
          info_sheet.minor.amount_euro === '' ||
          isNaN(info_sheet.minor.amount_euro.replace(',', '.'))
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
      if (this.id && this.validate(this.minor_info_sheet)) {
        api
          .post('/minors/minor/' + this.id, this.minor_info_sheet)
          .then(() => {
            if (
              this.isFirstPriceEditBool &&
              !!parseFloat(this.minor_info_sheet.minor.amount_euro) &&
              !!this.minor_info_sheet.minor.entry_date
            ) {
              this.addTariff(
                this.id,
                parseFloat(this.minor_info_sheet.minor.amount_euro),
                this.minor_info_sheet.minor.entry_date
                  .split('/')
                  .reverse()
                  .join('-')
              )
            } else {
              this.$router.push('/minors')
              this.showNotif(
                'positive',
                'Scheda informativa del minore salvata correttamente'
              )
            }
          })
          .catch(() => {
            this.showNotif(
              'warning',
              'Errore durante la modifica della scheda informativa del minore'
            )
          })
      }
    },
    addTariff(minorId, value, timestamp) {
      api
        .post('/minors/minor/' + minorId + '/price', {
          value: value,
          timestamp: timestamp
        })
        .then(() => {
          this.$router.push('/minors')
          this.showNotif(
            'positive',
            'Scheda informativa del minore salvata correttamente'
          )
        })
        .catch(() => {
          this.showNotif(
            'warning',
            'Non è stato possibile creare la tariffa per il minore'
          )
        })
    },

    watchDate(value, field) {
      this.minor_info_sheet.minor[field] = moment(value).format('DD/MM/YYYY')
    }
  }
}
</script>
<style scoped></style>
