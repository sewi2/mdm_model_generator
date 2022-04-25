if __name__ == '__main__':

    with open('VERSION', 'r') as version_file:
        version = version_file.read().strip()
        version_list = version.split('.')
        version_path = version_list[-1]
        if not version_path.isdigit():
            raise TypeError('Version path must be integer')
        path = int(version_path) + 1
        new_version = version_list[:-1]
        new_version.append(str(path))
        new_version = '.'.join(new_version)

    if new_version:
        with open('VERSION', 'w') as version_file:
            version_file.write(new_version)
