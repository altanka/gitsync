import inotify.adapters
import gitapi


def delete(repo, filename):
    repo.git_add("-u")
    repo.git_commit("Delete file %s" % filename, user="altanka", files=["."])
    repo.git_push()


def update(repo, filename):
    print("Adding: %s" % repo.git_add(filename))
    print("Commiting: %s" % repo.git_commit("Change file %s" % filename, user="altanka", files=["."]))
    print("Pushing: %s" % repo.git_push())


def start_listening():
    print("Listening workspace changes")

    repo = gitapi.Repo("/home/altanka/Acrome/testrepo")

    i = inotify.adapters.Inotify()

    i.add_watch('/home/altanka/Acrome/testrepo')

    excluded_types = ["IN_OPEN", "IN_CLOSE_NOWRITE", "IN_ACCESS", "IN_MODIFY"]
    excluded_names = [".swp", ".~", ".ipynb_checkpoints"]

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event
        print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(
            path, filename, type_names))
        if [name for name in excluded_types if name in type_names]:
            print("Excluded file")
            continue
        if [name for name in excluded_names if filename.endswith(name) or filename.startswith(name) or not filename]:
            print("Excluded file")
            continue

        if "IN_DELETE" in type_names:
            delete(repo, filename)
        else:
            update(repo, filename)


if __name__ == '__main__':
    start_listening()
