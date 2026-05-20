"""PlantUML skinparam strings for SysML v2 diagram types."""

SYSML_FLOW_CONFIGS = {
    "sysml_bdd": """\
skinparam class<<PartDef>> {
    BackgroundColor #DDEEFF
    BorderColor #336699
}
skinparam class<<Part>> {
    BackgroundColor #BBDDFF
    BorderColor #336699
}
hide empty members
left to right direction
""",
    "sysml_ibd": """\
skinparam component<<Part>> {
    BackgroundColor #BBDDFF
    BorderColor #336699
}
skinparam rectangle<<ibd>> {
    BackgroundColor transparent
    BorderColor #336699
}
""",
    "sysml_req": """\
skinparam class<<requirement>> {
    BackgroundColor #FFF0CC
    BorderColor #CC9900
}
hide empty members
""",
}
