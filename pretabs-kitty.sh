# Start kitty with four preconfigured tabs and specific tab names:
kitty @ set-tab-title 'Tab1'
kitty @ launch --type=tab --tab-title "Tab2" --keep-focus
kitty @ focus-tab --match 'title:Tab2'
kitty @ launch --type=tab --tab-title "Tab3" --keep-focus
kitty @ focus-tab --match 'title:Tab3'
kitty @ launch --type=tab --tab-title "Tab4" --keep-focus
kitty @ focus-tab --match 'title:Tab4'
