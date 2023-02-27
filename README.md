# SCARLET
## What it is
SCARLET (Simulated Cyber Attack Range for Leveraging Education and Training) is a cyber range designed to provide a safe, simulated environment for general security testing and training. SCARLET provides a novel _type system_ with which a user can design _scenarios_. Each _scenario_ can be thought of as a state of a system.

Currently, components that a user can define in a _scenario_ (or system) include:
- Devices present in the system and the configuration/flavor for each devices
- Applications/Services present in the system and the configuration/properties for each application/service
- Components that are specific to a cyber attack scenario, e.g. a vulnerability.
Specific component types that a user can declare can be found in `test-playbooks/types`.

Additionally, a user can specify the _relationship_ between each components to affect the order in which they are configured and initiated.
Specific relationships currently supported can be found in `test-playbooks/types`.
