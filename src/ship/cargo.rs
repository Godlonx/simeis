use std::collections::BTreeMap;

use serde::Serialize;

use super::resources::Resource;

#[derive(Default, Serialize)]
pub struct ShipCargo {
    pub capacity: f64,
    pub usage: f64,

    resources: BTreeMap<Resource, f64>,
}

impl ShipCargo {
    pub fn with_capacity(cap: f64) -> ShipCargo {
        ShipCargo {
            usage: 0.0,
            capacity: cap,
            resources: BTreeMap::new(),
        }
    }

    pub fn slowing_ratio(&self) -> f64 {
        // let usage_ratio = self.usage / self.capacity;
        // TODO (#12)    Cargo slows down speed of ship
        0.0
    }

    pub fn add_resource(&mut self, res: &Resource, amnt: f64) {
        log::debug!("Added {amnt} {res:?} to cargo");
        let add = res.volume() * amnt;
        if (self.usage + add) > self.capacity {
            self.usage = self.capacity;
        } else if self.usage == self.capacity {
            return;
        } else {
            self.usage += add;
        }

        if let Some(stock) = self.resources.get_mut(res) {
            *stock += amnt;
        } else {
            self.resources.insert(*res, amnt);
        }
    }

    pub fn is_full(&self) -> bool {
        self.usage == self.capacity
    }
}
