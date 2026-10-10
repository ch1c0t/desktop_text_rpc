require "json"
require "option_parser"
require "hobby-rpc"

socket = ENV["DESKTOP_TEXT_RPC_SOCKET"]? ||
  Path.home.join(".local/share/desktop-text-rpc/socket").to_s
display = ENV["DISPLAY"]?
OptionParser.parse do |opts|
  opts.banner = "Usage: desktop-text-rpc-client [options] present TEXT | recognize"
  opts.on("--socket PATH", "Unix socket path") { |value| socket = value }
  opts.on("--display DISPLAY", "X11 display to capture") { |value| display = value }
  opts.on("-h", "--help", "Show help") { puts opts; exit }
end

command = ARGV.shift? || "present"
rpc = HobbyRPC::Client.new(socket)
begin
  result = case command
  when "present"
    text = ARGV.shift? || abort("Missing text to search")
    rpc.call("TextPresent", {
      "text" => text, "display" => display,
      "case_sensitive" => false, "min_confidence" => 0.5,
    })
  when "recognize"
    rpc.call("RecognizeDesktop", {"display" => display})
  else
    abort("Unknown command: #{command}")
  end
  puts result.to_pretty_json
ensure
  rpc.close
end
