import asyncio
import fastapi

import databuilder, modelhandler

app = fastapi.FastAPI()

model_handler = modelhandler.ModelHandler('./models/model.h5')
data_builder = model_handler.data_builder

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
            status_code=404
        )
    return {
        'data': {
            'state_name': state_name,
            'predictions': predictions.tolist(),
            'timestamps': time.tolist(),
            'usages': usage.tolist()
        }
    }
