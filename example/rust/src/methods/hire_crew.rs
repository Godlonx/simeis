use crate::sdk::{get_id, SimeisSDK};
use crate::methods::job::JobType;


pub fn hire_new_crew(sdk: &SimeisSDK, station_id: u64, job: JobType) -> Result<u64, serde_json::Value> {
    let operator = sdk.hire_crew(station_id, job.get_name())?;
    let operator_id = get_id(&operator);
    Ok(operator_id)
}
