
import optparse
import sys
import util_cli

from cluster_manager import ClusterManager


def parse_command():
    """Parses a couchbase-cli command and routes the request to the appropriate handler

    Returns true if the command was handled"""
    if len(sys.argv) == 1:
        return False

    command = None
    if sys.argv[1] == "server-list":
        command = ServerList()
    else:
        return False

    options, args = command.parse(sys.argv[2:])
    errors = command.execute(options, args)
    if errors:
        for error in errors:
            print error

    return True


class Command(object):
    def __init__(self):
        self.parser = optparse.OptionParser()
        self.parser.add_option("-c", "--cluster", dest="host", help="The hostname of the Couchbase cluster")
        self.parser.add_option("-u", "--username", dest="username", help="The username for the Couchbase cluster")
        self.parser.add_option("-p", "--password", dest="password", help="The password for the Couchbase cluster")
        self.parser.add_option("-d", "--debug", dest="debug", action="store_true",
                               help="Run the command with extra logging")
        self.parser.add_option("-s", "--ssl", dest="ssl", action="store_true",
                               help="Use ssl when connecting to Couchbase")

    def parse(self, args):
        return self.parser.parse_args(args)

    def execute(self, options, args):
        raise NotImplementedError

    def help(self):
        pass


class ServerList(Command):
    def __init__(self):
        super(ServerList, self).__init__()
        self.parser.set_usage('couchbase-cli server-list [options]')

    def parse(self, args):
        return super(ServerList, self).parse(args)

    def execute(self, options, args):
        server, port = util_cli.hostport(options.host)
        cm = ClusterManager(server, port, options.username, options.password, options.ssl)
        result, errors = cm.pools('default')
        if errors:
            return errors

        nodes = result['nodes']
        for node in nodes:
            if node.get('otpNode') is None:
                raise Exception("could not access node")

            print '%s %s %s %s' % (node['otpNode'],
                                   node['hostname'],
                                   node['status'],
                                   node['clusterMembership'])

        return None

    def help(self):
        pass