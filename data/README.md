# CarScope — Dataset Guidelines & Data Privacy

## Bundled Sample Dataset
CarScope comes pre-packaged with a sample vehicle dataset located at `data/sample_cars.csv`.
This dataset contains 60+ realistic vehicle listings across major manufacturers, model years, prices, mileage, fuel types, transmissions, engine displacement, horsepower, fuel economy, body types, and locations.

## Supplying a Custom CSV File
You can load any custom vehicle dataset CSV directly into CarScope using the file uploader in the sidebar.

### Data Privacy & Local Execution
- **100% Local Processing**: All uploaded CSV files are loaded and processed locally within your Python / Streamlit session. No car records, personal information, or statistics leave your computer or get transmitted to remote cloud databases.
- **Unmodified Raw Data**: CarScope never mutates or overwrites your original CSV file on disk.

### Recommended & Supported Columns
CarScope uses an intelligent column aliasing system. Your CSV columns can have any of the following names:

| Canonical Field | Description | Common Column Aliases Recognized |
|---|---|---|
| `make` | Vehicle Manufacturer | `Make`, `manufacturer`, `brand`, `company` |
| `model` | Vehicle Model Name | `Model`, `car_model`, `model_name`, `trim` |
| `year` | Production / Registration Year | `Year`, `model_year`, `prod_year`, `reg_year` |
| `price` | Listed Price | `Price`, `selling_price`, `cost`, `msrp`, `value`, `amount` |
| `mileage` | Odometer Reading | `Mileage`, `odometer`, `km_driven`, `distance`, `miles` |
| `fuel_type` | Engine Fuel Category | `Fuel_Type`, `fuel`, `fueltype`, `engine_fuel` |
| `transmission` | Gearbox / Transmission Type | `Transmission`, `gearbox`, `gear_type`, `trans` |
| `engine_size` | Engine Displacement (L) | `Engine_Size_L`, `engine`, `displacement`, `vol_cc` |
| `horsepower` | Engine Power (hp) | `Horsepower`, `power`, `hp`, `max_power` |
| `mpg` | Fuel Economy | `MPG`, `fuel_economy`, `consumption`, `kml` |
| `body_type` | Body Style | `Body_Type`, `body`, `vehicle_type`, `car_type` |
| `condition` | Vehicle Condition | `Condition`, `status`, `usage` |
| `location` | Listing City/State | `Location`, `city`, `state`, `region` |

If your CSV uses custom or non-standard column headers, expand the **⚙️ Dataset Column Mapping** section in the sidebar to manually select column mappings.
