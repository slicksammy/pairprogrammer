class Planner
  require 'net/http'
  require 'json'

  def respond(message)
    uri = URI('http://example.com')

    http = Net::HTTP.new(uri.host, uri.port)
    req = Net::HTTP::Post.new(uri.path, { 'Content-Type' => 'application/json' })
    req.body = { message: message }.to_json
    response = http.request(req)

    response.body
  end

  def help_message
    "Usage: planner respond MESSAGE

Options:
  --help   Show this help message.
"
  end
end

if ARGV.include?('--help')
  planner = Planner.new
  puts planner.help_message
  exit
end

if ARGV.empty?
  puts 'No arguments provided. Please provide a command.'
else
  command = ARGV[0]
  argument = ARGV[1..-1]

  planner = Planner.new

  case command
  when 'planner'
    sub_command = argument.shift
    case sub_command
    when 'respond'
      message = argument.join(' ')
      puts planner.respond(message)
    else
      puts 'Unknown sub-command. Try "planner respond MESSAGE"'
    end
  else
    puts 'Unknown command. Try "planner respond MESSAGE"'
  end
end