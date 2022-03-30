"""Stream type classes for tap-trustrace."""
import requests

from datetime import date
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers
from singer_sdk.helpers.jsonpath import extract_jsonpath


from tap_trustrace.client import trustraceStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
MATERIALS_CUSTOM_FIELDS = [
    "cfPhysicalInformationFactsThicknessValue1",
    "cfPhysicalInformationStrengthElongationYDirectionInValue3",
    "cfPhysicalInformationStrengthElongationYDirectionInValue2",
    "cfPhysicalInformationStrengthElongationYDirectionInValue1",
    "cfHiggMsiHiggMappingMaterialNameValue1",
    "cfSustainabilityInformationSourcingRenewableResourceInValue1",
    "cfCommercialInformationCommercialInformationRevisionValue1",
    "cfPhysicalInformationAgeingYellowingStandardAstmD1148Value1",
    "cfPhysicalInformationStrengthElongationXDirectionInValue3",
    "cfPhysicalInformationStrengthElongationXDirectionInValue2",
    "cfPhysicalInformationStrengthElongationXDirectionInValue1",
    "cfHiggMsiHiggScoresGlobalWarmingMidpointsKgCo2EqValue1",
    "cfPhysicalInformationWaterMoistureAndColourColorFastnessValue1",
    "cfPhysicalInformationWaterMoistureAndColourColorFastnessValue2",
    "cfPhysicalInformationWaterMoistureAndColourColorFastnessValue3",
    "cfCommercialInformationCommercialInformationAreaOfUsageValue1",
    "cfPhysicalInformationResistanceAbrasionDryValue1",
    "cfPhysicalInformationResistanceAbrasionDryValue2",
    "cfPhysicalInformationResistanceAbrasionDryValue3",
    "cfPhysicalInformationStrengthTearStrengthXDirectionValue1",
    "cfPhysicalInformationStrengthTearStrengthXDirectionValue2",
    "cfPhysicalInformationStrengthTearStrengthXDirectionValue3",
    "cfPhysicalInformationStrengthTearStrengthXDirectionValue4",
    "cfCommercialInformationCommercialInformationStatusValue1",
    "cfCommercialInformationCommercialInformationGroupValue1",
    "cfHiggMsiHiggMappingMaterialIdValue1",
    "cfSustainabilityInformationTreatmentProcessesLowImpactTreatmentInValue1",
    "cfSustainabilityInformationTreatmentProcessesLowImpactTreatmentInValue2",
    "cfSustainabilityInformationTreatmentProcessesDyeingProcessInValue1",
    "cfSustainabilityInformationTreatmentProcessesDyeingProcessInValue2",
    "cfSustainabilityInformationSourcingSourcingOfRawMaterialValue1",
    "cfCommercialInformationCommercialInformationDateOfRevisionValue1",
    "cfSustainabilityInformationOtherCuttingWasteValue1",
    "cfPhysicalInformationStrengthTearStrengthYDirectionValue1",
    "cfPhysicalInformationStrengthTearStrengthYDirectionValue2",
    "cfPhysicalInformationStrengthTearStrengthYDirectionValue3",
    "cfPhysicalInformationStrengthTearStrengthYDirectionValue4",
    "cfSustainabilityInformationRecyclingRecycledContentInValue1",
    "cfPhysicalInformationFactsThicknessValue2",
    "cfSustainabilityInformationSourcingCircularityInValue1",
    "cfSustainabilityInformationRecyclingRecycledContentInValue2",
    "cfSustainabilityInformationRecyclingRecycledContentInValue3",
    "cfSustainabilityInformationRecyclingRecycledContentInValue4",
]

STYLES_CUSTOM_FIELDS = [
    "certificatesRequired",
    "sustainabilityLabels",
    "suppliers",
    "billOfMaterials",
    "productCategories",
]


class MaterialsStream(trustraceStream):

    name = "materials"
    path = "/materials/get-all-materials"
    primary_keys = ["articleUid"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "materials.json"
    rest_method = "POST"

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        self.records_jsonpath = "$.data.materials[*]"
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def post_process(self, row: dict, context: Optional[dict]) -> dict:
        """As needed, append or transform raw data to match expected structure."""
        row["extraction_date"] = date.today().strftime("%Y-%m-%d")
        if "customFields" in row:
            for cf in MATERIALS_CUSTOM_FIELDS:
                if cf in row["customFields"]:
                    row[cf] = row["customFields"][cf][0]
                else:
                    row[cf] = None
        else:
            for cf in MATERIALS_CUSTOM_FIELDS:
                row[cf] = None
        return row


class StylesStream(trustraceStream):

    name = "styles"
    path = "/styles/get-all-styles"
    primary_keys = ["styleUid"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "styles.json"
    rest_method = "POST"

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        self.records_jsonpath = "$.data.styles[*]"
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def post_process(self, row: dict, context: Optional[dict]) -> dict:
        """As needed, append or transform raw data to match expected structure."""
        row["extraction_date"] = date.today().strftime("%Y-%m-%d")
        for field in STYLES_CUSTOM_FIELDS:
            if (field not in row) or (len(row[field]) == 0):
                row[field] = None
            elif field == "billOfMaterials":
                for obj in row["billOfMaterials"]:
                    if "areaOfUsage" not in obj:
                        obj["areaOfUsage"] = None
                    obj["quantity_value"] = obj["quantity"]["value"]
                    obj["quantity_unit"] = obj["quantity"]["unit"]
        return row