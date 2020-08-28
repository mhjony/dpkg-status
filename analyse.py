limits, lines = [], []

with open('/var/lib/dpkg/status') as fp:
    lines = fp.read().splitlines()

    begin, end = 0, 0

    for line in lines:
        if len(line.rstrip()) == 0:           
            limits.append((begin, end))
            begin = end + 1
        end += 1

# uqnique dependencies 
unique_dependencies = set(())
# associative arrays -> package: [dependencies]
package_dependencies = {}
# generate --> unique_dependencies & package_dependencies
for limit in limits:
    begin, end = limit
    
    name, depends = '', ''
    
    for line in lines[begin: end]:
        # name
        query_param = 'Package: '
        if line.startswith(query_param):
            name = line[len(query_param):].strip()

        # dependencies
        if 'Depends: ' in line:
            query_param = 'Pre-Depends: '
            if query_param in line:                
                depends += line[len(query_param):].strip()
            query_param = 'Depends: '
            if query_param in line:
                depends += line[len(query_param):].strip()

    unique_dependencies.add(name)

    dpns = depends.split(',')
    package_dependencies[name] = []
    for dpn in dpns:
        dp = dpn[0:dpn.find('(')].strip()
        if len(dp) > 0 and not dp in package_dependencies[name]:
            package_dependencies[name].append(dp)

# reverse dependencies
reverse_dependencies = {}
# p: [d]
for ud in unique_dependencies:
    reverse_dependencies[ud] = []
    for p,d in package_dependencies.items():
        if ud in d:
            reverse_dependencies[ud].append(p)

#print(len(reverse_dependencies))
html = '<table border="1px">'
html += '<tr><th>Package</th><th>Description</th><th>Dependencies</th><th>Reverse Dependencies</th></tr>'

for limit in limits:
    begin, end = limit

    html += '<tr border="1px">'
    name, description, depends, links, rd_links = '', '', '', '', ''
    
    for line in lines[begin: end]:
        # name
        query_param = 'Package: '
        if line.startswith(query_param):
            name = line[len(query_param):].strip()
        # description
        query_param = 'Description: '
        if line.startswith(query_param) or line.startswith(' ') and not line.startswith(' /'):
            if line.startswith(query_param):
                description += line[len(query_param):].strip()
            else:
                description += line[0:].strip()
        # dependencies
        if 'Depends: ' in line:
            query_param = 'Pre-Depends: '
            if query_param in line:                
                depends += line[len(query_param):].strip()
            query_param = 'Depends: '
            if query_param in line:
                depends += line[len(query_param):].strip()

    html += '<td id="{}" class="package">{}</td>'.format(name, name)
    html += '<td class="description">{description}</td>'.format(description=description)

    dpns = depends.split(',')
    package_dependencies[name] = []
    for dpn in dpns:
        dp = dpn[0:dpn.find('(')].strip()
        pipe = dp.split(' | ')
        for dp in pipe:
            if dp in unique_dependencies:
                dp = dp
            else:
                dp = pipe[0]     
        links += '<a href="#{dp}">{dp}</a>, '.format(dp= dp.strip())
    if len(links) > 0:
    	html += '<td class="dependencies">{}</td>'.format(links[:-2])
    else:
    	html += '<td class="dependencies"></td>'
    
    for rd in reverse_dependencies[name]:
        rd_links += '<a href="#{rd}">{rd}</a>, '.format(rd= rd.strip())
    if len(links) > 0:
        html += '<td class="reverse_dependencies">{}</td>'.format(rd_links[:-2])
    else:
        html += '<td class="reverse_dependencies"></td>'

    html += '</tr>'

html += '</table>'
print(html)