import asyncio
import fastapi
import aiohttp
import numpy as np

import databuilder, modelhandler, cea, util

app = fastapi.FastAPI()

model_handler = modelhandler.ModelHandler('./models/model.h5')
data_builder = model_handler.data_builder

@app.on_event('startup')
async def startup_hook():
    app.session = aiohttp.ClientSession()
    app.cea_client = cea.CEAClient(app.session)
    await app.cea_client.populate_cache()

@app.get('/api/states/list/')
async def get_all_states():
    return {'state_list': databuilder.STATE_LIST}


@app.get('/api/states/{state_name}/')
async def state_entry(state_name: str):
    try:
        time, usage = await asyncio.get_running_loop().run_in_executor(None, data_builder.build_data, state_name)
        predictions = await asyncio.get_running_loop().run_in_executor(None, model_handler.make_predictions, state_name)
    except ValueError as err:
        return fastapi.responses.JSONResponse(
            {
                'data': str(err),
                'state_name': state_name
            },
            status_code=404 # the only error that can happen here is a 404 in the event an invalid state was specified
        )
    if state_name in app.cea_client.state_cache:
        state_name_cea = state_name
    else:
        state_name_cea = util.MANUAL_MAPPING[state_name]
    
    state_latest_monthly_availability = app.cea_client.state_cache[state_name_cea][-1].energy_availability

    recorded_monthly_energy_usage = await asyncio.get_running_loop().run_in_executor(
        None,
        util.aggregate_last_month_usage,
        usage
    )

    last_20_day_usage = await asyncio.get_running_loop().run_in_executor(
        None,
        util.aggregate_last_n_day_usage,
        usage,
        20
    )

    prediction_sum = await asyncio.get_event_loop().run_in_executor(
        None, 
        np.sum,
        predictions
    )
    predicted_monthly_energy_usage = last_20_day_usage + prediction_sum
    
    return {
        'data': {
            'state_name': state_name,
            'predictions': predictions.tolist(),
            'monthly_availability': state_latest_monthly_availability,
            'recorded_monthly_usage': recorded_monthly_energy_usage,
            'predicted_monthly_usage': predicted_monthly_energy_usage,
            'timestamps': time.tolist(),
            'usages': usage.tolist()
        }
    }
