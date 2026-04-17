pub enum JobType {
    Pilot,
    Operator,
    Trader,
}

impl JobType {
    pub fn get_name(&self) -> &str {
        match self {
            JobType::Pilot => "pilot",
            JobType::Operator => "operator",
            JobType::Trader => "trader",
        }
    }
}