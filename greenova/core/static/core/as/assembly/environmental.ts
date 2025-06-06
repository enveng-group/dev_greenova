// Environmental-specific AssemblyScript functions
// Advanced environmental data processing and analysis

/**
 * Environmental compliance calculation functions
 */

/**
 * Calculate environmental risk score based on multiple factors
 * @param emissionLevel - Current emission level (0-100)
 * @param regulatoryLimit - Regulatory limit for emissions
 * @param historicalTrend - Historical trend (-100 to 100, negative=improving)
 * @param environmentalSensitivity - Environmental sensitivity factor (1-10)
 * @returns Risk score (0-1000)
 */
export function calculateEnvironmentalRisk(
  emissionLevel: f32,
  regulatoryLimit: f32,
  historicalTrend: f32,
  environmentalSensitivity: f32
): i32 {
  let riskScore: f32 = 0;

  // Base risk from emission level vs regulatory limit
  const complianceRatio = emissionLevel / regulatoryLimit;
  if (complianceRatio > 1.0) {
    riskScore += 300 * (complianceRatio - 1.0); // Penalty for exceeding limits
  } else if (complianceRatio > 0.8) {
    riskScore += 200 * (complianceRatio - 0.8) / 0.2; // Risk for approaching limits
  } else if (complianceRatio > 0.6) {
    riskScore += 100 * (complianceRatio - 0.6) / 0.2; // Moderate risk
  }

  // Historical trend factor
  if (historicalTrend > 0) {
    riskScore += historicalTrend * 2; // Worsening trend increases risk
  }

  // Environmental sensitivity multiplier
  riskScore *= environmentalSensitivity / 5.0;

  // Cap at maximum risk score
  return i32(riskScore > 1000 ? 1000 : riskScore);
}

/**
 * Calculate carbon footprint from activity data
 * @param activityDataPtr - Pointer to activity data array
 * @param emissionFactorsPtr - Pointer to emission factors array
 * @param length - Length of arrays
 * @returns Total CO2 equivalent in tonnes
 */
export function calculateCarbonFootprint(
  activityDataPtr: usize,
  emissionFactorsPtr: usize,
  length: i32
): f32 {
  if (length <= 0) return 0;

  const activityData = load<Float32Array>(activityDataPtr);
  const emissionFactors = load<Float32Array>(emissionFactorsPtr);

  let totalEmissions: f32 = 0;

  for (let i = 0; i < length; i++) {
    const activity = unchecked(activityData[i]);
    const factor = unchecked(emissionFactors[i]);
    totalEmissions += activity * factor;
  }

  return totalEmissions;
}

/**
 * Water quality assessment functions
 */

/**
 * Calculate water quality index from multiple parameters
 * @param parametersPtr - Pointer to water quality parameters array
 * @param standardsPtr - Pointer to water quality standards array
 * @param weightsPtr - Pointer to parameter weights array
 * @param length - Number of parameters
 * @returns Water Quality Index (0-100, higher is better)
 */
export function calculateWaterQualityIndex(
  parametersPtr: usize,
  standardsPtr: usize,
  weightsPtr: usize,
  length: i32
): f32 {
  if (length <= 0) return 0;

  const parameters = load<Float32Array>(parametersPtr);
  const standards = load<Float32Array>(standardsPtr);
  const weights = load<Float32Array>(weightsPtr);

  let weightedSum: f32 = 0;
  let totalWeight: f32 = 0;

  for (let i = 0; i < length; i++) {
    const parameter = unchecked(parameters[i]);
    const standard = unchecked(standards[i]);
    const weight = unchecked(weights[i]);

    // Calculate sub-index (0-100 scale)
    let subIndex: f32;
    if (parameter <= standard) {
      subIndex = 100 * (parameter / standard);
    } else {
      // Penalty for exceeding standards
      subIndex = 100 * (1 - (parameter - standard) / standard);
      if (subIndex < 0) subIndex = 0;
    }

    weightedSum += subIndex * weight;
    totalWeight += weight;
  }

  return totalWeight > 0 ? weightedSum / totalWeight : 0;
}

/**
 * Air quality monitoring functions
 */

/**
 * Calculate Air Quality Index (AQI) from pollutant concentrations
 * @param pollutantConcentrations - Array of pollutant concentrations
 * @param pollutantStandards - Array of pollutant standards
 * @param length - Number of pollutants
 * @returns AQI value (0-500)
 */
export function calculateAirQualityIndex(
  pollutantConcentrations: usize,
  pollutantStandards: usize,
  length: i32
): i32 {
  if (length <= 0) return 0;

  const concentrations = load<Float32Array>(pollutantConcentrations);
  const standards = load<Float32Array>(pollutantStandards);

  let maxAQI: f32 = 0;

  for (let i = 0; i < length; i++) {
    const concentration = unchecked(concentrations[i]);
    const standard = unchecked(standards[i]);

    // Calculate individual AQI for this pollutant
    let aqi: f32;
    const ratio = concentration / standard;

    if (ratio <= 1.0) {
      // Good to Moderate (0-100)
      aqi = ratio * 100;
    } else if (ratio <= 2.0) {
      // Unhealthy for Sensitive Groups (101-150)
      aqi = 100 + (ratio - 1.0) * 50;
    } else if (ratio <= 3.0) {
      // Unhealthy (151-200)
      aqi = 150 + (ratio - 2.0) * 50;
    } else if (ratio <= 4.0) {
      // Very Unhealthy (201-300)
      aqi = 200 + (ratio - 3.0) * 100;
    } else {
      // Hazardous (301-500)
      aqi = 300 + (ratio - 4.0) * 200;
      if (aqi > 500) aqi = 500;
    }

    if (aqi > maxAQI) maxAQI = aqi;
  }

  return i32(maxAQI);
}

/**
 * Waste management calculation functions
 */

/**
 * Calculate waste diversion rate
 * @param recycledWeight - Weight of recycled materials
 * @param compostedWeight - Weight of composted materials
 * @param reusedWeight - Weight of reused materials
 * @param totalWasteWeight - Total waste weight
 * @returns Diversion rate as percentage (0-100)
 */
export function calculateWasteDiversionRate(
  recycledWeight: f32,
  compostedWeight: f32,
  reusedWeight: f32,
  totalWasteWeight: f32
): f32 {
  if (totalWasteWeight <= 0) return 0;

  const divertedWeight = recycledWeight + compostedWeight + reusedWeight;
  return (divertedWeight / totalWasteWeight) * 100;
}

/**
 * Energy efficiency calculation functions
 */

/**
 * Calculate energy efficiency ratio
 * @param energyConsumed - Energy consumed in kWh
 * @param productionOutput - Production output (units)
 * @param baselineEfficiency - Baseline efficiency ratio
 * @returns Efficiency improvement percentage
 */
export function calculateEnergyEfficiency(
  energyConsumed: f32,
  productionOutput: f32,
  baselineEfficiency: f32
): f32 {
  if (productionOutput <= 0 || baselineEfficiency <= 0) return 0;

  const currentEfficiency = productionOutput / energyConsumed;
  const improvement = ((currentEfficiency - baselineEfficiency) / baselineEfficiency) * 100;

  return improvement;
}

/**
 * Biodiversity assessment functions
 */

/**
 * Calculate Shannon diversity index
 * @param speciesCountsPtr - Pointer to species count array
 * @param speciesCount - Number of species
 * @returns Shannon diversity index
 */
export function calculateShannonDiversity(
  speciesCountsPtr: usize,
  speciesCount: i32
): f32 {
  if (speciesCount <= 0) return 0;

  const counts = load<Int32Array>(speciesCountsPtr);
  let totalIndividuals: i32 = 0;

  // Calculate total individuals
  for (let i = 0; i < speciesCount; i++) {
    totalIndividuals += unchecked(counts[i]);
  }

  if (totalIndividuals <= 0) return 0;

  let diversity: f32 = 0;

  for (let i = 0; i < speciesCount; i++) {
    const count = unchecked(counts[i]);
    if (count > 0) {
      const proportion = f32(count) / f32(totalIndividuals);
      diversity -= proportion * Mathf.log2(proportion);
    }
  }

  return diversity;
}

/**
 * Climate data processing functions
 */

/**
 * Calculate temperature anomaly
 * @param temperaturesPtr - Pointer to temperature data array
 * @param baselinePtr - Pointer to baseline temperature array
 * @param length - Length of arrays
 * @returns Average temperature anomaly in degrees Celsius
 */
export function calculateTemperatureAnomaly(
  temperaturesPtr: usize,
  baselinePtr: usize,
  length: i32
): f32 {
  if (length <= 0) return 0;

  const temperatures = load<Float32Array>(temperaturesPtr);
  const baseline = load<Float32Array>(baselinePtr);

  let totalAnomaly: f32 = 0;

  for (let i = 0; i < length; i++) {
    const temp = unchecked(temperatures[i]);
    const base = unchecked(baseline[i]);
    totalAnomaly += temp - base;
  }

  return totalAnomaly / f32(length);
}
