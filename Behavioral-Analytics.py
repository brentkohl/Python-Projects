import psutil

conn_counts = {}
totalConns = 0


def buildBaseLine():
    for p in psutil.pids():
        proc = psutil.Process(p)
        name = proc.name()
        hasConns = int(len(proc.connections()) > 0)
        if name in conn_counts:
            (connected, total) = conn_counts[name]
            conn_counts[name] = (connected + hasConns, total + 1)
        else:
            conn_counts[name] = (hasConns, 1)


threshold = 0.5


def checkConnections():
    for p in psutil.pids():
        proc = psutil.Process(p)
        name = proc.name()
        hasConns = len(proc.connections()) > 0
        if hasConns:
            if name in conn_counts:
                (connected, total) = conn_counts[name]
                prob = connected / total
                if prob < threshold:
                    print(
                        "Process %s has network connction at %f probability"
                        % (name, prob)
                    )
            else:
                print("New process %s has network conneciton" % name)
        else:
            if name in conn_counts:
                (connected, total) = conn_counts[name]
                prob = 1 - (connected / total)
                if prob < threshold:
                    print(
                        "Process %s doesn't have network connction at %f probability"
                        % (name, prob)
                    )


buildBaseLine()
checkConnections()
