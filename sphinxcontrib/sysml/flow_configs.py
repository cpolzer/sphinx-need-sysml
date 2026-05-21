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
    # === New in feature 002-full-sysml-diagrams ===
    "sysml_stm": """\
skinparam state {
    BackgroundColor #EEEEDD
    BorderColor #888866
}
skinparam state<<choice>> {
    BackgroundColor #FFEEBB
    BorderColor #CC9900
}
skinparam state<<junction>> {
    BackgroundColor #DDDDDD
    BorderColor #888888
}
""",
    "sysml_act": """\
skinparam activity {
    BackgroundColor #FFEEDD
    BorderColor #CC9966
    DiamondBackgroundColor #FFE0AA
    DiamondBorderColor #CC8800
}
skinparam partition {
    BackgroundColor #FAF6EE
    BorderColor #CC9966
}
""",
    "sysml_sd": """\
skinparam sequence {
    ParticipantBackgroundColor #E0E8F0
    ParticipantBorderColor #336699
    ArrowColor #336699
    LifeLineBorderColor #888888
    GroupBackgroundColor #F4F4FF
    GroupBorderColor #336699
}
""",
    "sysml_uc": """\
skinparam usecase {
    BackgroundColor #FFEEDD
    BorderColor #CC8800
}
skinparam actor {
    BackgroundColor #EEEECC
    BorderColor #886600
}
skinparam rectangle {
    BorderColor #336699
}
left to right direction
""",
    "sysml_pkg": """\
skinparam package {
    BackgroundColor #EEEEFF
    BorderColor #336699
}
skinparam ArrowColor #336699
""",
    "sysml_par": """\
skinparam class<<constraint>> {
    BackgroundColor #FFF0DC
    BorderColor #CC9966
    RoundCorner 12
}
skinparam class<<valueproperty>> {
    BackgroundColor #E8F4FF
    BorderColor #336699
}
hide empty members
""",
}
