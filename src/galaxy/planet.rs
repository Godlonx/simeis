use serde::Serialize;

use crate::ship::resources::Resource;

use super::SpaceCoord;

#[derive(Serialize, Debug)]
pub struct Planet {
    pub position: SpaceCoord,
    temperature: u16,
    solid: bool,
}

impl Planet {
    pub fn random<R: rand::Rng>(coord: SpaceCoord, rng: &mut R) -> Planet {
        Planet {
            solid: rng.random_bool(0.4),
            temperature: rng.random(),
            position: coord,
        }
    }

    pub fn resource_present(&self, resource: &Resource) -> bool {
        if self.solid {
            matches!(resource, Resource::Stone | Resource::Iron)
        } else {
            matches!(resource, Resource::Helium | Resource::Ozone)
        }
    }
}
