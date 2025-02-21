<!-- eslint-disable vue/no-v-html -->
<template>
  <q-page class="q-mx-xl">
    <div class="row">
      <div class="col-12">
        <div class="row items-center q-mb-md">
          <div class="col">
            <Heading :title="'Catalogo Incentivi'" />
          </div>
          <div class="col-auto">
            <q-btn
              flat
              color="primary"
              icon="refresh"
              :loading="loading"
              @click="fetchIncentives(true)">
              <q-tooltip>Aggiorna catalogo</q-tooltip>
            </q-btn>
          </div>
        </div>
      </div>
    </div>

    <q-expansion-item
      v-model="showFilters"
      group="filters"
      switch-toggle-side
      dense
      class="filter-panel q-mb-md">
      <template #header>
        <div class="filter-header full-width cursor-pointer">
          <q-icon name="filter_list" color="primary" size="24px" />
          <div class="text-h6 text-primary q-my-none">Filtri</div>
          <div v-if="lastUpdated" class="text-caption text-grey q-ml-sm">
            Ultimo aggiornamento: {{ formatDateTime(lastUpdated) }}
          </div>
          <q-space />
          <div class="text-caption text-grey">
            <transition name="filter-count">
              <span v-if="hasActiveFilters">
                {{ activeFilterCount }} filtri attivi
                <q-btn
                  flat
                  dense
                  round
                  color="grey"
                  icon="clear_all"
                  size="sm"
                  @click.stop="clearAllFilters">
                  <q-tooltip>Cancella tutti i filtri</q-tooltip>
                </q-btn>
              </span>
            </transition>
          </div>
          <q-icon
            :name="showFilters ? 'expand_less' : 'expand_more'"
            color="primary"
            size="24px"
            class="q-ml-sm transition-transform"
            :class="{ 'rotate-180': !showFilters }" />
        </div>
      </template>

      <q-card>
        <q-card-section>
          <div class="row q-col-gutter-md">
            <div class="col-12 col-sm-6 col-md-4">
              <div class="text-subtitle2 q-mb-sm">Settore attività</div>
              <q-select
                v-model="selectedSectors"
                :options="sectorOptions"
                multiple
                outlined
                dense
                options-dense
                use-chips
                input-debounce="0"
                behavior="menu"
                class="custom-select"
                popup-content-class="custom-select-popup"
                hide-dropdown-icon
                clearable
                emit-value
                map-options
                :style="{ minHeight: '56px' }"
                @update:model-value="onSelectInput($event, 'sectors')">
                <template #append>
                  <q-icon name="expand_more" class="cursor-pointer" />
                </template>
                <template #selected-item="scope">
                  <q-chip
                    removable
                    dense
                    color="primary"
                    text-color="white"
                    class="select-chip"
                    @remove="scope.removeAtIndex(scope.index)">
                    {{ scope.opt }}
                  </q-chip>
                </template>
                <template #option="{ itemProps, opt, selected, toggleOption }">
                  <q-item
                    v-bind="itemProps"
                    clickable
                    @click="toggleOption(opt)">
                    <q-item-section>
                      <q-item-label>{{ opt }}</q-item-label>
                    </q-item-section>
                    <q-item-section side>
                      <q-checkbox
                        :model-value="selected"
                        color="primary"
                        @click.stop
                        @update:model-value="toggleOption(opt)" />
                    </q-item-section>
                  </q-item>
                </template>
                <template #no-option>
                  <q-item>
                    <q-item-section class="text-grey">
                      Nessun risultato trovato
                    </q-item-section>
                  </q-item>
                </template>
              </q-select>
            </div>

            <div class="col-12 col-sm-6 col-md-4">
              <div class="text-subtitle2 q-mb-sm">Regione</div>
              <q-select
                v-model="selectedRegions"
                :options="regionOptions"
                multiple
                outlined
                dense
                options-dense
                use-chips
                input-debounce="0"
                behavior="menu"
                class="custom-select"
                popup-content-class="custom-select-popup"
                hide-dropdown-icon
                clearable
                :style="{ minHeight: '56px' }"
                @update:model-value="onSelectInput($event, 'regions')">
                <template #append>
                  <q-icon name="expand_more" class="cursor-pointer" />
                </template>
                <template #selected-item="scope">
                  <q-chip
                    removable
                    dense
                    color="primary"
                    text-color="white"
                    class="select-chip"
                    @remove="scope.removeAtIndex(scope.index)">
                    {{ scope.opt }}
                  </q-chip>
                </template>
                <template #option="{ itemProps, opt, selected, toggleOption }">
                  <q-item
                    v-bind="itemProps"
                    clickable
                    @click="toggleOption(opt)">
                    <q-item-section>
                      <q-item-label>{{ opt }}</q-item-label>
                    </q-item-section>
                    <q-item-section side>
                      <q-checkbox
                        :model-value="selected"
                        color="primary"
                        @click.stop
                        @update:model-value="toggleOption(opt)" />
                    </q-item-section>
                  </q-item>
                </template>
                <template #no-option>
                  <q-item>
                    <q-item-section class="text-grey">
                      Nessun risultato trovato
                    </q-item-section>
                  </q-item>
                </template>
              </q-select>
            </div>

            <div class="col-12 col-sm-6 col-md-4">
              <div class="text-subtitle2 q-mb-sm">Forma di supporto</div>
              <q-select
                v-model="selectedSupportForms"
                :options="supportFormOptions"
                multiple
                outlined
                dense
                options-dense
                use-chips
                input-debounce="0"
                behavior="menu"
                class="custom-select"
                popup-content-class="custom-select-popup"
                hide-dropdown-icon
                clearable
                :style="{ minHeight: '56px' }"
                @update:model-value="onSelectInput($event, 'supportForms')">
                <template #append>
                  <q-icon name="expand_more" class="cursor-pointer" />
                </template>
                <template #selected-item="scope">
                  <q-chip
                    removable
                    dense
                    color="primary"
                    text-color="white"
                    class="select-chip"
                    @remove="scope.removeAtIndex(scope.index)">
                    {{ scope.opt }}
                  </q-chip>
                </template>
                <template #option="{ itemProps, opt, selected, toggleOption }">
                  <q-item
                    v-bind="itemProps"
                    clickable
                    @click="toggleOption(opt)">
                    <q-item-section>
                      <q-item-label>{{ opt }}</q-item-label>
                    </q-item-section>
                    <q-item-section side>
                      <q-checkbox
                        :model-value="selected"
                        color="primary"
                        @click.stop
                        @update:model-value="toggleOption(opt)" />
                    </q-item-section>
                  </q-item>
                </template>
                <template #no-option>
                  <q-item>
                    <q-item-section class="text-grey">
                      Nessun risultato trovato
                    </q-item-section>
                  </q-item>
                </template>
              </q-select>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-expansion-item>

    <div class="row q-mt-md">
      <div class="col-12">
        <q-table
          v-model:pagination="pagination"
          class="catalogo-table"
          :rows="filteredRows"
          :columns="columns"
          row-key="title"
          :loading="loading"
          :rows-per-page-options="[5, 8, 10, 15, 25, 50]">
          <template #body-cell-title="props">
            <q-td>
              <q-tooltip>{{ props.value }}</q-tooltip>
              {{ truncateText(props.value, 50) }}
            </q-td>
          </template>

          <template #body-cell-categories="props">
            <q-td class="text-center">
              <template
                v-for="category in props.row.categories"
                :key="category">
                <q-chip
                  color="primary"
                  text-color="white"
                  size="sm"
                  class="q-ma-xs">
                  {{ category }}
                </q-chip>
              </template>
            </q-td>
          </template>

          <template #body-cell-status="props">
            <q-td class="text-center">
              <q-chip
                :color="getStatusColor(calculateStatus(props.row))"
                text-color="white"
                size="sm">
                {{ calculateStatus(props.row) }}
              </q-chip>
            </q-td>
          </template>

          <template #body-cell-sectors="props">
            <q-td class="text-center">
              <template v-for="sector in props.value" :key="sector">
                <q-chip
                  color="primary"
                  text-color="white"
                  size="sm"
                  class="q-ma-xs">
                  {{ sector }}
                </q-chip>
              </template>
            </q-td>
          </template>

          <template #body-cell-regions="props">
            <q-td class="text-center">
              <q-chip
                v-if="props.value"
                color="primary"
                text-color="white"
                size="sm"
                class="q-ma-xs">
                {{ props.value }}
              </q-chip>
            </q-td>
          </template>

          <template #body-cell-actions="props">
            <q-td class="text-center">
              <q-btn
                v-if="!isIncentiveSaved(props.row)"
                flat
                round
                dense
                color="primary"
                icon="save"
                :loading="props.row.saving"
                @click="saveIncentive(props.row)">
                <q-tooltip>Salva incentivo</q-tooltip>
              </q-btn>
              <q-btn
                flat
                round
                dense
                color="primary"
                icon="launch"
                size="sm"
                :href="'https://www.incentivi.gov.it/' + props.row.link"
                target="_blank"
                title="Apri link incentivo"
                class="q-ml-sm">
                <q-tooltip>Apri link</q-tooltip>
              </q-btn>
              <q-btn
                flat
                round
                dense
                color="primary"
                icon="analytics"
                class="q-mx-sm"
                @click="openAnalyzeDialog(props.row)">
                <q-tooltip>Analizza</q-tooltip>
              </q-btn>
            </q-td>
          </template>

          <template #no-data="{ message }">
            <div class="full-width row flex-center text-primary q-gutter-sm">
              <div v-if="message === 'Loading...'">{{ message }}</div>
              <div v-else>
                <q-icon size="2em" name="sentiment_dissatisfied" />
                <span>
                  {{
                    errorMsg
                      ? 'Impossibile caricare gli incentivi al momento..'
                      : 'Nessun incentivo presente ...'
                  }}
                </span>
              </div>
            </div>
          </template>
        </q-table>
      </div>
    </div>

    <q-dialog v-model="saveDialog.show" persistent>
      <q-card style="min-width: 350px">
        <q-card-section>
          <div class="text-h6">Salva Incentivo</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <div class="text-subtitle1 q-mb-md">
            {{ saveDialog.incentive?.title }}
          </div>
          <div class="text-body2">
            Confermi di voler salvare questo incentivo?
          </div>
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn
            v-close-popup
            flat
            label="Annulla"
            :disable="saveDialog.processing" />
          <q-btn
            flat
            label="Salva"
            :loading="saveDialog.processing"
            @click="confirmSaveIncentive" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Analyze Dialog -->
    <q-dialog v-model="analyzeDialog.show" persistent>
      <q-card style="min-width: 500px; max-width: 80vw">
        <q-card-section class="row items-center">
          <div class="text-h6">Analisi Incentivo</div>
          <q-space />
          <q-btn v-close-popup icon="close" flat round dense />
          <q-btn
            v-if="hasCachedAnalysis"
            icon="delete"
            flat
            round
            dense
            @click="clearAnalysisCache" />
        </q-card-section>

        <q-card-section>
          <div v-if="analyzeDialog.processing" class="text-center q-pa-md">
            <q-spinner color="primary" size="3em" />
            <div class="text-body1 q-mt-sm">
              {{
                analyzeDialog.currentStep === 'scraping'
                  ? 'Scraping della pagina Bandi in corso...'
                  : 'Analisi del testo in corso...'
              }}
            </div>
          </div>

          <div v-else-if="analyzeDialog.error" class="text-negative q-mb-md">
            <div class="text-h6 q-mb-sm">
              {{
                analyzeDialog.currentStep === 'scraping'
                  ? 'Scraping Bandi Fallito'
                  : 'Analisi del Testo Fallita'
              }}
            </div>
            {{ analyzeDialog.error }}
          </div>

          <div
            v-else-if="!analyzeDialog.analysis && !hasCachedAnalysis"
            class="text-center q-pa-md">
            <div class="text-body1 q-mb-sm">
              L'analisi può richiedere fino a 1 minuto.
            </div>
            <div class="text-caption text-grey-7">
              Puoi chiudere questa finestra e tornare più tardi per vedere i
              risultati.
            </div>
          </div>

          <div v-else-if="analyzeDialog.analysis" class="analysis-content">
            <div class="analysis-text" v-html="renderedAnalysis"></div>
          </div>
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn
            v-close-popup
            flat
            label="CHIUDI"
            :disable="analyzeDialog.processing" />
          <q-btn
            v-if="!analyzeDialog.analysis && !analyzeDialog.processing"
            color="primary"
            label="ANALIZZA"
            :loading="analyzeDialog.processing"
            @click="analyzeIncentive" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import Heading from 'components/Heading.vue'
import { api } from 'src/boot/axios'
import { useQuasar } from 'quasar'
import { ref } from 'vue'
import { _regions, _sectors } from 'src/const/incentivi'
import { useStore } from 'vuex'
import { SUPPORT_FORM_OPTIONS } from 'src/const/incentivi'
import { marked } from 'marked'

export default {
  name: 'Catalogo',
  components: {
    Heading
  },
  setup() {
    const store = useStore()
    const $q = useQuasar()
    const loading = ref(true)
    const errorMsg = ref(false)

    return {
      store,
      loading,
      errorMsg,
      showNotif(type, message) {
        $q.notify({
          type,
          message,
          position: 'top-right',
          timeout: 1000
        })
      }
    }
  },
  data() {
    return {
      rows: [],
      columns: [
        {
          name: 'title',
          align: 'left',
          label: 'Titolo',
          field: 'title',
          sortable: true
        },
        {
          name: 'categories',
          align: 'left',
          label: 'Categorie',
          field: 'categories'
        },
        {
          name: 'status',
          align: 'center',
          label: 'Stato',
          field: row => this.calculateStatus(row),
          sortable: true
        },
        // {
        //   name: 'sectors',
        //   align: 'left',
        //   label: 'Settori',
        //   field: row => this.getSectorNames(row.activity_sector)
        // },
        // {
        //   name: 'regions',
        //   align: 'left',
        //   label: 'Regioni',
        //   field: row => this.getRegionName(row.full_data?.regions)
        // },
        {
          name: 'open_date',
          align: 'center',
          label: 'Data Apertura',
          field: 'open_date',
          format: val => this.formatDate(val),
          sortable: true
        },
        {
          name: 'close_date',
          align: 'center',
          label: 'Data Chiusura',
          field: 'close_date',
          format: val => this.formatDate(val),
          sortable: true
        },
        {
          name: 'actions',
          align: 'center',
          label: 'Azioni'
        }
      ],
      pagination: {
        rowsPerPage: 8
      },
      selectedSectors: [],
      selectedRegions: [],
      selectedSupportForms: [],
      sectors: _sectors,
      regions: _regions,
      supportForms: SUPPORT_FORM_OPTIONS,
      isCached: false,
      lastUpdated: null,
      saveDialog: {
        show: false,
        processing: false,
        incentive: null
      },
      analyzeDialog: {
        show: false,
        processing: false,
        incentive: null,
        analysis: null,
        error: null,
        currentStep: null
      },
      showFilters: false
    }
  },
  computed: {
    sectorOptions() {
      return Object.keys(this.sectors)
    },
    regionOptions() {
      return Object.keys(this.regions)
    },
    supportFormOptions() {
      return Object.values(SUPPORT_FORM_OPTIONS)
    },
    filteredRows() {
      return this.rows.filter(row => {
        const matchesSectors =
          this.selectedSectors.length === 0 ||
          this.selectedSectors.some(sector =>
            row.activity_sector?.includes(this.sectors[sector])
          )

        const matchesRegions =
          this.selectedRegions.length === 0 ||
          this.selectedRegions.some(
            region => row.full_data?.regions === this.regions[region]
          )

        const matchesSupportForms =
          this.selectedSupportForms.length === 0 ||
          this.selectedSupportForms.includes(
            this.supportForms[row.support_form]
          )

        return matchesSectors && matchesRegions && matchesSupportForms
      })
    },
    hasActiveFilters() {
      return (
        this.selectedSectors.length > 0 ||
        this.selectedRegions.length > 0 ||
        this.selectedSupportForms.length > 0
      )
    },
    activeFilterCount() {
      return (
        this.selectedSectors.length +
        this.selectedRegions.length +
        this.selectedSupportForms.length
      )
    },
    hasCachedAnalysis() {
      return (
        this.analyzeDialog.incentive?.link &&
        localStorage.getItem(this.analyzeDialog.incentive.link) !== null
      )
    },
    renderedAnalysis() {
      if (!this.analyzeDialog.analysis) return ''
      marked.setOptions({
        gfm: true,
        breaks: true,
        headerIds: false,
        mangle: false,
        pedantic: false,
        sanitize: false,
        smartLists: true,
        smartypants: false,
        langPrefix: 'language-'
      })
      return marked(this.analyzeDialog.analysis)
    }
  },
  mounted() {
    const storedData = this.$store.getters.getIncentives
    if (storedData.data.length > 0) {
      this.rows = storedData.data
      this.isCached = storedData.cached
      this.lastUpdated = storedData.lastUpdated
      this.loading = false
    } else {
      this.fetchIncentives()
    }
  },
  methods: {
    isIncentiveSaved(incentive) {
      const userIncentives = this.$store.getters.getUserIncentives.data
      return userIncentives.some(saved => saved.id === incentive.id)
    },
    async fetchIncentives(forceRefresh = false) {
      if (!forceRefresh && this.rows.length > 0) {
        return
      }

      this.loading = true
      try {
        const response = await api.get('scrapper/incentives', {
          params: { force_refresh: forceRefresh }
        })
        const data = response.data.data || []
        const lastUpdated = response.data.last_updated || null
        const cached = response.data.cached || false
        const jobStatus = response.data.job_status
        const jobId = response.data.job_id

        if (jobStatus === 'running' && jobId) {
          this.$q.notify({
            type: 'info',
            message:
              'Aggiornamento incentivi in corso. Attendere circa 1 minuto per il completamento.',
            position: 'top',
            timeout: 5000
          })
          this.pollJobStatus(jobId)
        }

        this.$store.commit('setIncentives', {
          data,
          lastUpdated,
          cached
        })

        this.rows = data
        this.isCached = cached
        this.lastUpdated = lastUpdated
      } catch (error) {
        this.$q.notify({
          type: 'negative',
          message: 'Errore nel caricamento degli incentivi',
          position: 'top',
          timeout: 3000
        })
      } finally {
        this.loading = false
      }
    },

    async pollJobStatus(jobId) {
      const pollInterval = 20000 // Poll every 20 seconds
      const maxAttempts = 15 // Maximum 5 minutes of polling (20s * 15 = 5min)

      let attempts = 0
      const poll = async () => {
        try {
          const response = await api.get('scrapper/incentives')
          const jobStatus = response.data.job_status

          if (jobStatus !== 'running' || attempts >= maxAttempts) {
            // Job completed or max attempts reached, refresh data
            await this.fetchIncentives()
            return
          }

          attempts++
          setTimeout(poll, pollInterval)
        } catch (error) {
          console.error('Error polling job status:', error)
        }
      }

      poll()
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('it-IT', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      })
    },
    calculateStatus(row) {
      const now = new Date()

      const openDate = row.open_date ? new Date(row.open_date) : null
      const closeDate = row.close_date ? new Date(row.close_date) : null

      if (!openDate) return 'Non Disponibile'
      if (now < openDate) {
        return 'In Arrivo'
      } else if (!closeDate || now <= closeDate) {
        return 'Attivo'
      } else {
        return 'Scaduto'
      }
    },
    getStatusColor(status) {
      if (!status) return 'grey'
      const statusLower = status.toLowerCase()
      if (statusLower === 'attivo') return 'positive'
      if (statusLower === 'scaduto') return 'negative'
      if (statusLower === 'in arrivo') return 'warning'
      if (statusLower === 'non disponibile') return 'grey'
      return 'grey'
    },
    getSectorNames(sectorIds) {
      if (!sectorIds) return []
      const sectorEntries = Object.entries(this.sectors)
      return sectorIds
        .map(id => sectorEntries.find(([_, value]) => value === id)?.[0])
        .filter(Boolean)
    },
    getRegionName(regionId) {
      if (!regionId) return ''
      const regionEntry = Object.entries(this.regions).find(
        ([_, value]) => value === regionId
      )
      return regionEntry ? regionEntry[0] : ''
    },
    applyFilters() {
      this.$forceUpdate()
    },
    getSelectDisplayValue(selected) {
      if (!selected || selected.length === 0) return ''
      if (selected.length <= 2) {
        return selected.join(', ')
      }
      return `${selected.length} valori selezionati`
    },
    onSelectInput(val, type) {
      if (type === 'sectors') {
        this.selectedSectors = val || []
      } else if (type === 'regions') {
        this.selectedRegions = val || []
      } else {
        this.selectedSupportForms = val || []
      }
      this.$nextTick(() => {
        this.applyFilters()
      })
    },
    clearSelections(type) {
      switch (type) {
        case 'sectors':
          this.selectedSectors = []
          break
        case 'regions':
          this.selectedRegions = []
          break
        case 'supportForms':
          this.selectedSupportForms = []
          break
      }
      this.applyFilters()
    },
    truncateText(text, maxLength) {
      if (!text) return ''
      return text.length > maxLength
        ? text.substring(0, maxLength) + '...'
        : text
    },
    formatDateTime(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return new Intl.DateTimeFormat('it-IT', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date)
    },
    async saveIncentive(row) {
      this.saveDialog.incentive = row
      this.saveDialog.show = true
    },

    async confirmSaveIncentive() {
      if (!this.saveDialog.incentive) return

      this.saveDialog.processing = true
      const row = this.saveDialog.incentive

      try {
        const response = await api.post('scrapper/incentives', {
          id: row.id,
          title: row.title,
          link: row.link,
          activity_sector: row.activity_sector || [],
          categories: row.categories || [],
          sectors: row.sectors || [],
          regions: row.regions || [],
          scopes: row.scopes || [],
          open_date: row.open_date,
          close_date: row.close_date,
          support_form: row.support_form,
          description: row.description,
          status: this.calculateStatus(row),
          metadata: {
            source: row.source,
            last_updated: new Date().toISOString(),
            original_data: row
          }
        })

        const currentUserIncentives =
          this.$store.getters.getUserIncentives.data || []
        this.$store.commit('setUserIncentives', {
          data: [...currentUserIncentives, response.data.data],
          lastUpdated: new Date().toISOString()
        })

        this.$q.notify({
          type: 'positive',
          message: 'Incentivo salvato con successo',
          position: 'top',
          timeout: 2000
        })

        this.saveDialog.show = false
      } catch (error) {
        let errorMessage = "Errore durante il salvataggio dell'incentivo"

        if (error.response) {
          switch (error.response.status) {
            case 400:
              errorMessage = 'Dati non validi'
              break
            case 409:
              errorMessage = 'Incentivo già esistente'
              break
            case 500:
              errorMessage = 'Errore del server'
              break
          }
        }

        this.$q.notify({
          type: 'negative',
          message: errorMessage,
          position: 'top',
          timeout: 3000
        })
      } finally {
        this.saveDialog.processing = false
      }
    },
    openUrl(url) {
      if (url) {
        window.open(url, '_blank')
      }
    },
    clearAllFilters() {
      this.selectedSectors = []
      this.selectedRegions = []
      this.selectedSupportForms = []
      this.applyFilters()
    },
    openAnalyzeDialog(incentive) {
      this.analyzeDialog.incentive = incentive
      this.analyzeDialog.error = null
      this.analyzeDialog.processing = false
      this.analyzeDialog.analysis = ''
      this.analyzeDialog.currentStep = null
      const cachedAnalysis = localStorage.getItem(incentive.link)
      if (cachedAnalysis) {
        this.analyzeDialog.analysis = cachedAnalysis
      }

      this.analyzeDialog.show = true
    },

    async analyzeIncentive() {
      this.analyzeDialog.processing = true
      this.analyzeDialog.error = null
      this.analyzeDialog.currentStep = 'scraping'
      const cachedAnalysis = localStorage.getItem(
        this.analyzeDialog.incentive.link
      )
      if (cachedAnalysis) {
        this.analyzeDialog.analysis = cachedAnalysis
        this.analyzeDialog.processing = false
        return
      }
      try {
        // Step 1: Scrape the text from the URL
        const scrapeResponse = await api.post('scrapper/analyze', {
          url:
            'https://www.incentivi.gov.it' + this.analyzeDialog.incentive.link
        })

        if (!scrapeResponse.data?.success) {
          throw new Error("Errore durante l'estrazione del testo")
        }

        // Step 2: Analyze the scraped text
        this.analyzeDialog.currentStep = 'analyzing'
        const analysisResponse = await api.post('scrapper/analyze-text', {
          text: scrapeResponse.data.text
        })

        if (analysisResponse.data?.success) {
          this.analyzeDialog.analysis = analysisResponse.data.analysis
          localStorage.setItem(
            this.analyzeDialog.incentive.link,
            analysisResponse.data.analysis
          )
        } else {
          throw new Error("Errore durante l'analisi dell'incentivo")
        }
      } catch (error) {
        console.error('Error analyzing incentive:', error)
        this.analyzeDialog.error =
          error.response?.data?.error ||
          error.message ||
          "Errore durante l'analisi dell'incentivo"
      } finally {
        this.analyzeDialog.processing = false
      }
    },
    clearAnalysisCache() {
      if (this.analyzeDialog.incentive?.link) {
        localStorage.removeItem(this.analyzeDialog.incentive.link)
        this.analyzeDialog.analysis = ''
        this.$q.notify({
          type: 'positive',
          message: 'Cache analisi cancellata',
          position: 'top-right',
          timeout: 2000
        })
      }
    }
  }
}
</script>

<style scoped>
.catalogo-table {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 16px;
}

:deep(.q-table__container) {
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

:deep(.q-table__card) {
  border-radius: 8px;
}

:deep(.q-table thead tr) {
  height: 48px;
}

:deep(.q-table tbody td) {
  height: 52px;
}

:deep(.q-table th) {
  font-weight: 500;
  font-size: 13px;
  color: rgba(0, 0, 0, 0.85);
}

:deep(.q-table td) {
  font-size: 13px;
  color: rgba(0, 0, 0, 0.65);
}

.custom-select {
  width: 100%;
}

.custom-select :deep(.q-field__control) {
  height: 56px;
  padding: 0 12px;
}

.custom-select :deep(.q-field__control-container) {
  padding-top: 4px;
  padding-bottom: 4px;
  overflow-y: auto;
  max-height: 56px;
  scrollbar-width: thin;
}

.custom-select :deep(.q-field__control-container::-webkit-scrollbar) {
  width: 4px;
}

.custom-select :deep(.q-field__control-container::-webkit-scrollbar-track) {
  background: transparent;
}

.custom-select :deep(.q-field__control-container::-webkit-scrollbar-thumb) {
  background: #ddd;
  border-radius: 4px;
}

.custom-select
  :deep(.q-field__control-container::-webkit-scrollbar-thumb:hover) {
  background: #ccc;
}

.select-chip {
  margin: 2px;
  max-width: calc(100% - 4px);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

:deep(.custom-select-popup) {
  max-height: 300px;
}

:deep(.q-menu) {
  max-width: none !important;
  min-width: 200px !important;
}

:deep(.q-virtual-scroll__content) {
  padding: 4px 0;
}

:deep(.q-item) {
  min-height: 40px;
  padding: 8px 12px;
}

:deep(.q-item:hover) {
  background: rgba(0, 0, 0, 0.03);
}

:deep(.q-checkbox) {
  padding: 0;
  margin-left: 8px;
}

.analysis-content {
  max-height: 60vh;
  overflow-y: auto;
  padding: 16px;
}

.analysis-text {
  line-height: 1.6;
  font-size: 14px;
  color: #2c3e50;
}

.analysis-text :deep(h1),
.analysis-text :deep(h2) {
  font-weight: 600;
  margin: 16px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid #eaecef;
}

.analysis-text :deep(h1) {
  font-size: 24px;
}

.analysis-text :deep(h2) {
  font-size: 20px;
}

.analysis-text :deep(h3) {
  font-size: 18px;
  font-weight: 600;
  margin: 16px 0;
}

.analysis-text :deep(p) {
  margin: 12px 0;
  line-height: 1.7;
}

.analysis-text :deep(ul),
.analysis-text :deep(ol) {
  padding-left: 24px;
  margin: 12px 0;
}

.analysis-text :deep(li) {
  margin: 8px 0;
}

.analysis-text :deep(pre) {
  background-color: #f6f8fa;
  border-radius: 6px;
  padding: 16px;
  overflow: auto;
  margin: 16px 0;
  font-family: monospace;
}

.analysis-text :deep(code) {
  background-color: #f6f8fa;
  padding: 3px 6px;
  border-radius: 3px;
  font-family: monospace;
}

.analysis-text :deep(blockquote) {
  margin: 16px 0;
  padding: 0 16px;
  color: #6a737d;
  border-left: 4px solid #dfe2e5;
}

.analysis-text :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: 16px 0;
}

.analysis-text :deep(table th),
.analysis-text :deep(table td) {
  border: 1px solid #dfe2e5;
  padding: 8px 12px;
  text-align: left;
}

.analysis-text :deep(table th) {
  background-color: #f6f8fa;
  font-weight: 500;
}

.analysis-text :deep(table tr:nth-child(2n)) {
  background-color: #f8f9fa;
}

.filter-panel :deep(.q-card) {
  padding: 16px;
}

.filter-panel :deep(.q-card__section) {
  padding: 0;
}

.text-subtitle2 {
  margin-bottom: 8px;
  font-size: 14px;
}

.filter-title-column {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.filter-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  transition: background-color 0.3s ease;
}

.filter-header:hover {
  background-color: rgba(0, 0, 0, 0.03);
}

.filter-panel {
  background: white;
  transition: all 0.3s ease;
  border-radius: 8px;
  overflow: hidden;
}

.filter-panel :deep(.q-expansion-item__container) {
  border: 1px solid #e0e0e0;
  transition: border-color 0.3s ease;
}

.filter-panel :deep(.q-expansion-item__container:hover) {
  border-color: var(--q-primary);
}

.transition-transform {
  transition: transform 0.3s ease;
}

.rotate-180 {
  transform: rotate(180deg);
}

:deep(.q-field--outlined .q-field__control) {
  border-radius: 8px;
  border-color: #e0e0e0;
  transition: border-color 0.3s ease;
}

:deep(.q-field--outlined .q-field__control:hover) {
  border-color: var(--q-primary);
}

:deep(.q-field--focused .q-field__control) {
  border-color: var(--q-primary);
  border-width: 2px;
}

:deep(.q-field__label) {
  font-size: 14px;
  color: #666;
}

.analysis-content :deep(h1) {
  font-size: 1.5rem;
  font-weight: 500;
  margin-bottom: 1rem;
  color: var(--q-primary);
}

.analysis-content :deep(h2) {
  font-size: 1.25rem;
  font-weight: 500;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
  color: var(--q-primary);
}

.analysis-content :deep(ul) {
  padding-left: 1.5rem;
  margin: 0.5rem 0;
}

.analysis-content :deep(li) {
  margin: 0.25rem 0;
}

.analysis-content :deep(p) {
  margin: 0.5rem 0;
  line-height: 1.5;
}

.analysis-content :deep(strong) {
  font-weight: 500;
  color: rgba(0, 0, 0, 0.85);
}
</style>
