sysfonts::font_add_google("Zilla Slab", "pf", regular.wt = 500)

hexSticker::sticker(
  subplot = ~ plot.new(),
  s_x = 1,
  s_y = 1,
  s_width = 0.1,
  s_height = 0.1,
  package = "tinyvdiff",
  p_x = 1,
  p_y = 1,
  p_size = 26,
  h_size = 1.2,
  p_family = "pf",
  p_color = "#F06060",
  h_fill = "#FFF9F2",
  h_color = "#F06060",
  dpi = 320,
  filename = "docs/assets/logo.png"
)
