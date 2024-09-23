def eval_step(state, batch):
    #
    return state.apply_fn({"params": state.params}, batch)
