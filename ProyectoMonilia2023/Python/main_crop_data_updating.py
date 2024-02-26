from crop_data_updating import CropDataUpdating

UPDATE_LOT_1 = "update_lot_1"
UPDATE_LOT_2 = "update_lot_2"
UPDATE_LOT_3 = "update_lot_3"
UPDATE_LOT_4 = "update_lot_4"
UPDATE_GENERAL_DATA = "update_general_data"
LOT_NAME_FOR_SAMPLING = "lot_1"

# Gets the data from the given lot name and then updates it using some sample data.
crop_data_updating = CropDataUpdating()
print("GET DATA")
response_data = crop_data_updating.post_update(service=UPDATE_LOT_1,
                                               data=crop_data_updating.generate_empty_lot_x_data(LOT_NAME_FOR_SAMPLING))
print(response_data)
print("POST UPDATE")
response_data = crop_data_updating.post_update(service=UPDATE_LOT_1,
                                               data=crop_data_updating.generate_lot_x_data(LOT_NAME_FOR_SAMPLING))
print(response_data)
# Gets the general data and then updates it using some sample data.
print("GET DATA")
response_data = crop_data_updating.post_update(service=UPDATE_GENERAL_DATA,
                                               data=crop_data_updating.generate_empty_general_data())
print(response_data)
print("POST UPDATE")
response_data = crop_data_updating.post_update(service=UPDATE_GENERAL_DATA,
                                               data=crop_data_updating.generate_general_data())
print(response_data)
