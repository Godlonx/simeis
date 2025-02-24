use serde::Serialize;

#[derive(Serialize, Default)]
pub struct ShipStats {
    pub speed: f64,
    pub fuel_consumption: f64,

    pub hull_usage_rate: f64,
}
