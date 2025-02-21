export const _sectors = {
  'Agricoltura, silvicoltura e pesca': '586',
  Agroalimentare: '474',
  'Moda e Tessile': '475',
  'Veicoli a motore e altri mezzi di trasporto': '480',
  'Chimica e Farmaceutica': '476',
  Elettronica: '478',
  Meccanica: '479',
  Metallurgia: '477',
  'Arredamento, Legno e Carta': '481',
  Edilizia: '249',
  'Fornitura di Energia, Acqua e Gestione dei Rifiuti': '250',
  Commercio: '482',
  ICT: '486',
  'Servizi di trasporto': '483',
  'Settore alberghiero': '484',
  Ristorazione: '485',
  Turismo: '488',
  Sanità: '489',
  Cultura: '487',
  'Altri servizi': '490',
  Artigianato: '260'
}

export const _regions = {
  Abruzzo: '218',
  Abroad: '587',
  Basilicata: '219',
  Calabria: '220',
  Campania: '221',
  'Emilia-Romagna': '222',
  'Friuli Venezia Giulia': '223',
  Lazio: '224',
  Liguria: '225',
  Lombardy: '226',
  Marche: '227',
  Molise: '228',
  Piedmont: '229',
  Apulia: '230',
  Sardinia: '231',
  Sicily: '232',
  Tuscany: '233',
  'Trentino-Alto Adige/South Tyrol': '234',
  Umbria: '235',
  'Aosta Valley/Aosta Valley': '236',
  Veneto: '237'
}

export const SUPPORT_FORM_OPTIONS = {
  271: 'Agevolazione fiscale',
  295: 'Capitale di rischio',
  264: 'Contributo/Fondo perduto',
  214: 'Interventi a garanzia',
  279: 'Prestito/Anticipo rimborsabile',
  579: 'Riduzione dei contributi di previdenza sociale'
}

export const getSectorName = code => {
  return Object.keys(_sectors).find(key => _sectors[key] === code) || code
}

export const getRegionName = code => {
  return Object.keys(_regions).find(key => _regions[key] === code) || code
}

export const getSectorOptions = () => {
  return Object.entries(_sectors).map(([label, value]) => ({
    label,
    value
  }))
}

export const getRegionOptions = () => {
  return Object.entries(_regions).map(([label, value]) => ({
    label,
    value
  }))
}
