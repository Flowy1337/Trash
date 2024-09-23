/**@file
 * As shown, each content array can have it own content array again, its advised to only handle kind and type here
 * Inputs can be defined in blocks.js
 *
 * @type {Object}
 * @property {string} kind - The kind of the toolbox, set to "categoryToolbox".
 * @property {Array} contents - The contents of the toolbox, containing different categories of blocks.
 * @property {Object} contents[] - Each category in the toolbox.
 * @property {string} contents[].kind - The kind of the category, set to "category".
 * @property {string} contents[].name - The name of the category, displayed in the toolbox.
 * @property {string} contents[].categorystyle - The CSS class applied to the category for styling.
 * @property {Array} contents[].contents - The blocks contained in this category.
 * @property {Object} contents[].contents[] - Each block within the category.
 * @property {string} contents[].contents[].kind - The kind of the block, set to "block".
 * @property {string} contents[].contents[].type - The type identifier for the block (e.g., controls_if, logic_compare).
 *
 *
 */
export const toolbox = {
  'kind': 'categoryToolbox',
  'contents': [
    {
      'kind': 'category',
      'name': 'Logic',
      'categorystyle': 'logic_category',
      'contents': [
        {
          'kind': 'block',
          'type': 'controls_if',
        },
        {
          'kind': 'block',
          'type': 'logic_compare',
        },
        {
          'kind': 'block',
          'type': 'logic_operation',
        },
        {
          'kind': 'block',
          'type': 'logic_negate',
        },
        {
          'kind': 'block',
          'type': 'logic_boolean',
        },
        {
          'kind': 'block',
          'type': 'logic_null',
        },
        {
          'kind': 'block',
          'type': 'logic_ternary',
        },
      ],
    },
    {
      'kind': 'category',
      'name': 'Classes',
      'categorystyle': 'procedure_category',
      'contents': [
        {
          'kind': 'block',
          'type': 'python_class'
        },
        {
          'kind': 'block',
          'type': 'python_function'
        },
        {
          'kind': 'block',
          'type': 'member'
        },
        {
          'kind': 'block',
          'type': 'Declaration'
        },

        {
          'kind': 'block',
          'type': 'python_class_attribute'
        },
        {
          'kind': 'block',
          'type': 'python_return'
        },
        {
          'kind': 'block',
          'type': 'cheatblock'
        },
        {
          'kind': 'block',
          'type': 'self',
          'inputs': {
            "func": {
              'shadow': {
                "type": 'math_number',
                'fields': {
                  'NUM': '',
                }
              },
              "inputsInline": true,
              "previousStatement": null,
              "nextStatement": null,
              "colour": 230
            },
          },
        },
        {'kind':'block','type':'comment'},


      ]
    },
    {
      'kind': 'category',
      'name': 'Loops',
      'categorystyle': 'loop_category',
      'contents': [
        {
          'kind': 'block',
          'type': 'python_loop'
        },
        {
          'kind': 'block',
          'type': 'controls_repeat_ext',
          'inputs': {
            'TIMES': {
              'shadow': {
                'type': 'math_number',
                'fields': {
                  'NUM': 10,
                },
              },
            },
          },
        },
        {
          'kind': 'block',
          'type': 'controls_whileUntil',
        },
        {
          'kind': 'block',
          'type': 'controls_for',
          'inputs': {
            'FROM': {
              'shadow': {
                'type': 'math_number',
                'fields': {
                  'NUM': 1,
                },
              },
            },
            'TO': {
              'shadow': {
                'type': 'math_number',
                'fields': {
                  'NUM': 10,
                },
              },
            },
            'BY': {
              'shadow': {
                'type': 'math_number',
                'fields': {
                  'NUM': 1,
                },
              },
            },
          },
        },
        {
          'kind': 'block',
          'type': 'controls_forEach',
        },
        {
          'kind': 'block',
          'type': 'controls_flow_statements',
        },
      ],
    },
    {
      'kind': 'category',
      'name': 'Math',
      'categorystyle': 'math_category',
      'contents': [
        {
          'kind': 'block',
          'type': 'math_number',
          'fields': {
            'NUM': 123,
          },
        },
        {
          'kind': 'block',
          'type': 'math_arithmetic',
          'inputs': {
            'A': {
              'shadow': {
                'type': 'math_number',
                'fields': {
                  'NUM': 1,
                },
              },
            },
            'B': {
              'shadow': {
                'type': 'math_number',
                'fields': {
                  'NUM': 1,
                },
              },
            },
          },
        },
        {
          'kind': 'block',
          'type': 'math_single',
          'inputs': {
            'NUM': {
              'shadow': {
                'type': 'math_number',
                'fields': {
                  'NUM': 9,
                },
              },
            },
          },
        },
        {
          'kind': 'block',
          'type': 'math_trig',
          'inputs': {
            'NUM': {
              'shadow': {
                'type': 'math_number',
                'fields': {
                  'NUM': 45,
                },
              },
            },
          },
        },
        {
          'kind': 'block',
          'type': 'math_constant',
        },
        {
          'kind': 'block',
          'type': 'math_number_property',
          'inputs': {
            'NUMBER_TO_CHECK': {
              'shadow': {
                'type': 'math_number',
                'fields': {
                  'NUM': 0,
                },
              },
            },
          },
        },
        {
          'kind': 'block',
          'type': 'math_round',
          'fields': {
            'OP': 'ROUND',
          },
          'inputs': {
            'NUM': {
              'shadow': {
                'type': 'math_number',
                'fields': {
                  'NUM': 3.1,
                },
              },
            },
          },
        },
        {
          'kind': 'block',
          'type': 'math_on_list',
          'fields': {
            'OP': 'SUM',
          },
        },
        {
          'kind': 'block',
          'type': 'math_modulo',
          'inputs': {
            'DIVIDEND': {
              'shadow': {
                'type': 'math_number',
                'fields': {
                  'NUM': 64,
                },
              },
            },
            'DIVISOR': {
              'shadow': {
                'type': 'math_number',
                'fields': {
                  'NUM': 10,
                },
              },
            },
          },
        },
        {
          'kind': 'block',
          'type': 'math_constrain',
          'inputs': {
            'VALUE': {
              'shadow': {
                'type': 'math_number',
                'fields': {
                  'NUM': 50,
                },
              },
            },
            'LOW': {
              'shadow': {
                'type': 'math_number',
                'fields': {
                  'NUM': 1,
                },
              },
            },
            'HIGH': {
              'shadow': {
                'type': 'math_number',
                'fields': {
                  'NUM': 100,
                },
              },
            },
          },
        },
        {
          'kind': 'block',
          'type': 'math_random_int',
          'inputs': {
            'FROM': {
              'shadow': {
                'type': 'math_number',
                'fields': {
                  'NUM': 1,
                },
              },
            },
            'TO': {
              'shadow': {
                'type': 'math_number',
                'fields': {
                  'NUM': 100,
                },
              },
            },
          },
        },
        {
          'kind': 'block',
          'type': 'math_random_float',
        },
        {
          'kind': 'block',
          'type': 'math_atan2',
          'inputs': {
            'X': {
              'shadow': {
                'type': 'math_number',
                'fields': {
                  'NUM': 1,
                },
              },
            },
            'Y': {
              'shadow': {
                'type': 'math_number',
                'fields': {
                  'NUM': 1,
                },
              },
            },
          },
        },
      ],
    },
    {
      'kind': 'category',
      'name': 'Variables',
      'colour': 340,
            'contents': [
        {
          'kind': 'block',
          'type': 'set_var'
        },
        {
          'kind': 'block',
          'type': 'get_variable'
        },

      ]
    },
    {
      'kind': 'category',
      'name': 'JAX Operations',
      'colour':'#FF69B4',
      'contents': [

        {
          'kind': 'block',
          'type': 'mean'
        },

      ]
    },

        {
          'kind': 'category',
          'name': 'Layers',
          'colour': 120,
          'contents': [
            {
              'kind': 'category',
              'name': 'Linear Modules',
              'colour': 230,
              'contents': [
                {'kind': 'block', 'type': 'Dense'},
                {'kind': 'block', 'type': 'Dense_General'},
                {'kind': 'block', 'type': 'reshape'},
                {'kind': 'block', 'type': 'Conv'},
                {'kind': 'block', 'type': 'ConvTranspose'},
                {'kind': 'block', 'type': 'conv_local'},
                {'kind': 'block', 'type': 'Embed'},
                {'kind': 'block', 'type': 'einsum'},

              ],
            },
            {
              'kind': 'category',
              'name': 'Pooling',
              'colour': 130,
              'contents': [
                {'kind': 'block', 'type': 'max_pool'},
                {'kind': 'block', 'type': 'avg_pool'},
                {'kind': 'block', 'type': 'pool'},


              ],
            },
            {
              'kind': 'category',
              'name': 'Normalisation',
              'colour': 50,
              'contents': [
                {'kind': 'block', 'type': 'BatchNorm'},
                {'kind': 'block', 'type': 'LayerNorm'},
                {'kind': 'block', 'type': 'GroupNorm'},
                {'kind': 'block', 'type': 'RMSNorm'},
                {'kind': 'block', 'type': 'SpectralNorm'},
                {'kind': 'block', 'type': 'InstanceNorm'},
                {'kind': 'block', 'type': 'WeightNorm'},


              ],
            },
            {
              'kind': 'category',
              'name': 'Combinators',
              'colour': 300,
              'contents': [
                {'kind': 'block', 'type': 'Sequential'}
              ],
            },
            {
              'kind': 'category',
              'name': 'Stochastic',
              'colour': 180,
              'contents': [
              {'kind': 'block', 'type': 'Dropout'},
              ],
            },
            {
              'kind': 'category',
              'name': 'Attention',
              'colour': 70,
              'contents': [
                {'kind': 'block', 'type': 'MultiHeadDotProductAttention'},
                {'kind': 'block', 'type': 'MultiHeadAttention'},
                {'kind': 'block', 'type': 'SelfAttention'},

                {'kind': 'block', 'type': 'dot_product_attention'},
                {'kind': 'block', 'type': 'make_attention_mask'},
                {'kind': 'block', 'type': 'makecausalmask'},
              ],
            },
            {
              'kind': 'category',
              'name': 'Recurrent',
              'colour': 100,
              'contents': [
                {'kind': 'block', 'type': 'RNNCellBase'},
                {'kind': 'block', 'type': 'LSTMCell'},
                {'kind': 'block', 'type': 'OptimizedLSTMCell'},
                {'kind': 'block', 'type': 'ConvLSTMCell'},
                {'kind': 'block', 'type': 'SimpleCell'},
                {'kind': 'block', 'type': 'GRUCell'},
                {'kind': 'block', 'type': 'MGUCell'},
                {'kind': 'block', 'type': 'RNN'},
                {'kind': 'block', 'type': 'Bidirectional'},
              ],
            },
          ],
        },
        {
          'kind': 'category',
          'name': 'Activation Functions',
          'colour':230,
          'contents': [
            {'kind': 'block', 'type': 'PReLU'},
            {
              'kind': 'block',
              'type': 'celu'
            },
            {
              'kind': 'block',
              'type': 'elu'
            },
            {
              'kind': 'block',
              'type': 'gelu_layer'
            },
            {
              'kind': 'block',
              'type': 'gelu'
            },
            {

              'kind': 'block',
              'type': 'glu_layer'
            },
            {
              'kind': 'block',
              'type': 'hard_sigmoid'
            },
            {
              'kind': 'block',
              'type': 'hard_silu'
            },
            {'kind': 'block', 'type': 'sigmoid'},
            {'kind': 'block', 'type': 'tanh'},
            {'kind': 'block', 'type': 'relu'},
            {'kind': 'block', 'type': 'hard_tanh'},
            {'kind': 'block', 'type': 'leaky_relu'},
            {'kind': 'block', 'type': 'log_sigmoid'},
            {'kind': 'block', 'type': 'log_softmax'},
            {'kind': 'block', 'type': 'logsumexp'},
            {'kind': 'block', 'type': 'one_hot'},
            {'kind': 'block', 'type': 'selu'},

            {'kind': 'block', 'type': 'silu'},
            {'kind': 'block', 'type': 'soft_sign'},
            {'kind': 'block', 'type': 'softmax'},
            {'kind': 'block', 'type': 'softplus'},
            {'kind': 'block', 'type': 'standardize'},
            {'kind': 'block', 'type': 'swish'},


            // Add more activation functions as needed
          ],
        },
        // Other blocks in the flax.linen package can go here

        {
          'kind': 'category',
          'name': 'Init/Apply',
          "colour":400,
          'contents': [
            {'kind': 'block', 'type': 'apply'},
            {'kind': 'block', 'type': 'init'},
            {'kind': 'block', 'type': 'init_with_output'}
          ],
        },
        {
          'kind': 'category',
          'name': 'Initializers',
          'colour':10,
          'contents': [{'kind': 'block', 'type': 'constant'},
            {'kind': 'block', 'type': 'delta_orthogonal'},
            {'kind': 'block', 'type': 'glorot_normal'},
            {'kind': 'block', 'type': 'glorot_uniform'},
            {'kind': 'block', 'type': 'he_normal'},
            {'kind': 'block', 'type': 'he_uniform'},
            {'kind': 'block', 'type': 'kaiming_normal'},
            {'kind': 'block', 'type': 'kaiming_uniform'},
            {'kind': 'block', 'type': 'lecun_normal'},
            {'kind': 'block', 'type': 'lecun_uniform'},
            {'kind': 'block', 'type': 'normal'},
            {'kind': 'block', 'type': 'truncated_normal'},
            {'kind': 'block', 'type': 'ones'},
            {'kind': 'block', 'type': 'ones_init'},
            {'kind': 'block', 'type': 'orthogonal'},
            {'kind': 'block', 'type': 'uniform'},
            {'kind': 'block', 'type': 'variance_scaling'},
            {'kind': 'block', 'type': 'xavier_normal'},
            {'kind': 'block', 'type': 'xavier_uniform'},
            {'kind': 'block', 'type': 'zeros'},
            {'kind': 'block', 'type': 'zeros_init'},

          ],
        },
        {
          'kind': 'category',
          'name': 'Transformation',
          'colour':500,
          'contents': [
            {'kind': 'block', 'type': 'vmap'},
            {'kind': 'block', 'type': 'scan'},
            {'kind': 'block', 'type': 'jit'},
            {'kind': 'block', 'type': 'remat'},
            {'kind': 'block', 'type': 'remat_scan'},
            {'kind': 'block', 'type': 'map_variables'},
            {'kind': 'block', 'type': 'jvp'},
            {'kind': 'block', 'type': 'vjp'},
            {'kind': 'block', 'type': 'custom_vjp'},
            {'kind': 'block', 'type': 'while_loop'},
            {'kind': 'block', 'type': 'cond'},
            {'kind': 'block', 'type': 'switch'},

          ],
        },
        {
          'kind': 'category',
          'name': 'Inspection',
          'colour':270,
          'contents': [
          {'kind': 'block', 'type': 'tabulate'},
          ],
        },
        {
          'kind': 'category',
          'name': 'Variable Dictionary',
          'colour':180,
          'contents': [
            {'kind': 'block', 'type': 'Variable'},
          ],
        },
        {
          'kind': 'category',
          'name': 'SPMD',
          "colour": 70,
          'contents': [{'kind': 'block', 'type': 'Partitioned'},
            {'kind': 'block', 'type': 'with_partitioning'},
            {'kind': 'block', 'type':'get_partition_spec'},
            {'kind': 'block', 'type': 'get_sharding'},
            {'kind': 'block', 'type': 'LogicallyPartitioned'},
            {'kind': 'block', 'type': 'logical_axis_rules'},
            {'kind': 'block', 'type': 'set_logical_axis_rules'},
            {'kind': 'block', 'type': 'get_logical_axis_rules'},
            {'kind': 'block', 'type': 'logical_to_mesh_axes'},
            {'kind': 'block', 'type': 'logical_to_mesh'},
            {'kind': 'block', 'type': 'logical_to_mesh_sharding'},
            {'kind': 'block', 'type': 'with_logical_constraint'},
            {'kind': 'block', 'type': 'with_logical_partitioning'},


          ],
        },
        {
          'kind': 'category',
          'name': 'Functions',
          'categorystyle': 'procedure_category',
          'custom': 'PROCEDURE',
        },
        {
          'kind': 'category',
          'name': 'Decorators',
          "colour": '#A52A2A',
          'contents': [
            {
              'kind': 'block',
              'type': 'nn_compact'
            },
            {
              'kind': 'block',
              'type': 'nn_nowrap'
            }

          ],
        },
        {
          'kind': 'category',
          'name': 'Profiling',
          'colour': '#FFA500',
          'contents': [
            {'kind': 'block', 'type': 'enable_named_call'},
            {'kind': 'block', 'type': 'disable_named_call'},
            {'kind': 'block', 'type': 'override_named_call'},


          ],
        },

  ]}
  