local config = {
	defaults = {
		theme = "dark",
		transparent = false,
		overrides = {},
	},
}

setmetatable(config, { __index = config.defaults })

return config
