model_arch_path = 'model-1.19246-0.603-symbol.json'
model_params_path = 'model-1.19246-0.603-0223.params'
ctx = mx.cpu()
symbol = mx.sym.load(model_arch_path)
inputs = mx.sym.var('data', dtype='float32')
value_out = symbol.get_internals()['value_tanh0_output']
policy_out = symbol.get_internals()['flatten0_output']
sym = mx.symbol.Group([value_out, policy_out])
net = mx.gluon.SymbolBlock(sym, inputs)
net.collect_params().load(model_params_path, ctx)
