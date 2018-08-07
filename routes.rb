require 'plezi'
require_relative 'app/controllers/eventstream.rb'
## 
# ws://0.0.0.0/notifications
Plezi.route '/notifications', EventStream
Plezi.route 'public/javascripts/client.js', :client
