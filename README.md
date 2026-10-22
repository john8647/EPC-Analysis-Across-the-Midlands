# ![Project banner](resources/banner.png)

# EPC Analysis Across the Midlands

An EPC is an energy certificate for a property in England, Wales or Northern Ireland. This includes homes, business properties and public buildings.

The certificate is a standardised document that rates a property’s energy efficiency on a scale from A (most efficient) to G (least efficient). It provides an estimate of typical energy costs, details the property's environmental impact, and outlines actionable recommendations to improve efficiency and reduce carbon emissions. In many countries, including the UK, an EPC is legally required whenever a building is constructed, sold, or rented, and remains valid for 10 years.

The UK government is legally bound to achieve Net Zero greenhouse gas emissions by 2050. Because residential heating and electricity account for roughly 20% of the UK's total carbon emissions, upgrading home energy efficiency is critical to meeting statutory carbon budget targets. Initiatives like the Warm Homes Plan and stricter Minimum Energy Efficiency Standards (MEES) aim to decarbonize housing and strengthen national energy security.

For homeowners and renters, higher efficiency translates directly to lower monthly utility bills. Better insulation, efficient heat sources, and smart controls reduce wasted energy, protecting household budgets from price volatility in global fuel markets

# Dataset

The dataset is Kaggles EPC ratings England July 2023, the database is one of the richest data on individual residential properties. With 92 features and 21 million properties from England its also very large.  
My chosen sample region is the Midlands covering Coventry and Birmingham postcode city area for demonstration purposes due to practicality with the current hardware resource constrains.
The aim of this project is to use advanced data analysis to demonstrate mining the data for possible actions. Using the feature available through Python library to communication the data and to dicuss the Ethical practice that also need to be considered.

# Business Requirements

Targeted Retrofits: Maximizing Government Grant Impact on Regional EPCs
This dashboard helps policy makers answer a critical question: Where and how should we allocate retrofit funding for maximum impact? By evaluating building age, property usage, and regional density, the tool determines the single upgrade that generates the highest EPC score gain per pound spent. Users can adjust an interactive budget slider to model cost estimates and identify the ideal target areas for government-funded campaigns.

# Ethical consideration.

So what are the consideration, knowing that in this public dataset there is no personal data, so no GDPR or sensitive data is stored. But we have to consider property‑level information, which creates indirect ethical concerns around how the data could be interpreted, repurposed, or used in ways that affect people or communities. The residents could be subject to unfair commercial targeting as EPC‑related features (age, insulation, heating type, efficiency) can be used to: identify neighbourhoods with older, colder homes and target those areas with aggressive sales campaigns.
Property upgrades can be expensive and if there is the potential to push expensive upgrades or exploit households with limited income it could lead to hardship.
This is a form of data‑enabled commercial pressure, not a privacy breach its just can be used in a way which is unfair or manipulative.
The dataset includes: fields property age, heating system, insulation, glazing, efficiency rating and location.
These features correlate strongly with: income, deprivation, rental vs owner‑occupied status likelihood of fuel poverty. So it can indirectly make implication. Then could lead to profiling an entire neighbourhoods which is ethically sensitive.
The dataset can unintentionally reinforce thinking like
“older homes are worse and therefore morally responsible for emissions”
“certain regions contribute more to carbon output”
“homeowners should bear the cost of upgrades”

But carbon responsibility is not evenly distributed — it’s shaped by:

- historical building standards
- landlord behaviour
- regional investment
- national policy
- global supply chains

Bias in Housing Stock Representation.
Also consider that some regions have more EPC‑recorded properties, this may be due to the nature of renting in the area and how local policy recommendations are enforced.
Also older homes may be over‑represented while rural areas may be under‑represented
In some areas rental properties may appear more frequently
This affects:

- regression accuracy
- clustering patterns
- fairness of conclusions
- policy recommendations

Misinterpretation and Overgeneralisation
A model trained on EPC features might lead people to:

- assume a home is “poor quality”
- assume a neighbourhood is “low income”
- assume certain homes are “high risk”
- make unfair comparisons between regions
- assume an increase in renting in an area will directly increase carbon emissions.

Misinterpretation of EPC‑related property data may distort housing market perceptions, potentially lowering the sale price of older homes or inflating the value of newer ones, thereby reducing affordability for prospective buyers.

So we have to consider some of these as risks relating to socioeconomic profiling, unfair commercial targeting, and misinterpretation of carbon responsibility.

## Hypothesis and how to validate?

## Section 1 - Exploring features that relate to energy.

We Identified from the data where results of "Poor" or "Very_Poor" these when related to either the walls, roof, windows or mainheating would result in a low score. Almost half is caused by poor wall insulation. Suggesting energy loss through the wall is the highest factor to a low EPC rating.

## Section 2 - Potential SAP Point Gain

Once an EPC assessment is complete, assessors highlight key upgrades to boost the rating. The SAP (Standard Assessment Procedure) each count as a point towards to final score. Through analytical modeling, we can single out the most effective feature to deliver the biggest performance jump. By evaluating high-impact measures like window upgrades, wall insulation, or loft insulation, we can isolate the single most effective improvement. Applying this targeted upgrade across a specific housing group clearly demonstrates its power to elevate EPC scores.

## Section 3 - Application

Government energy grants are targeted, meaning deployment strategy is just as critical as the upgrade itself. Our tool not only identifies the single most impactful feature to upgrade (windows, walls, or roof insulation), but also maps where to apply it. By segmenting housing and demographic datasets, we enable grant administrators to pinpoint target groups and maximize campaign outcomes.

## Background## Code not fixed.
