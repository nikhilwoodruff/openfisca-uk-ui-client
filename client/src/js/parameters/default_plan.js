const DEFAULT_PLAN = {
    basic_rate: {
      title: "Basic rate",
      description: "The basic rate is the first of three tax brackets on all income, after allowances are deducted.",
      default: 20,
      value: 20,
      summary: "Change the basic rate to @%",
      type: "rate"
    },
    higher_rate: {
      title: "Higher rate",
      description: "The higher rate is the middle tax bracket.",
      default: 40,
      value: 40,
      summary: "Change the higher rate to @%",
      type: "rate"
    },
    add_rate: {
      title: "Additional rate",
      description: "The additional rate is the highest tax bracket, with no upper bound.",
      default: 45,
      value: 45,
      summary: "Change the additional rate to @%",
      type: "rate"
    },
    basic_threshold: {
      title: "Basic rate threshold",
      description: "Lower threshold for the basic rate, on income after allowances (including the personal allowance) have been deducted.",
      default: 0,
      value: 0,
      max: 100000,
      summary: "Change the basic rate to £@/year",
      type: "yearly"
    },
    higher_threshold: {
      title: "Higher rate threshold",
      description: "The lower threshold for the higher rate of income tax (and therefore the upper threshold of the basic rate).",
      default: 37500,
      value: 37500,
      max: 200000,
      summary: "Change the higher rate to £@/year",
      type: "yearly"
    },
    add_threshold: {
      title: "Additional rate",
      description: "The lower threshold for the additional rate.",
      default: 150000,
      value: 150000,
      max: 1000000,
      summary: "Change the additional rate to £@/year",
      type: "yearly"
    },
    personal_allowance: {
      title: "Personal allowance",
      description: "The personal allowance is deducted from general income.",
      default: 12500,
      value: 12500,
      max: 25000,
      summary: "Change the personal allowance to £@/year",
      type: "yearly"
    },
    NI_main_rate: {
      title: "NI main rate",
      description: "The Class 1 NI main rate is paid on employment earnings between the Primary Threshold and the Upper Earnings Limit.",
      default: 12,
      value: 12,
      summary: "Change the NI main rate to @%",
      type: "rate"
    },
    NI_add_rate: {
      title: "NI additional rate",
      description: "The Class 1 NI additional rate is paid on employment earnings above the Upper Earnings Limit.",
      default: 2,
      value: 2,
      summary: "Change the NI additional rate to @%",
      type: "rate"
    },
    NI_PT: {
      title: "NI Primary Threshold",
      description: "The Primary Threshold is the lower bound for the main rate of NI.",
      default: 183,
      value: 183,
      max: 1000,
      summary: "Change the PT to £@/week",
      type: "weekly"
    },
    NI_UEL: {
      title: "NI Upper Earnings Limit",
      description: "The Upper Earnings Limit is the upper bound for the main rate of NI.",
      default: 962,
      value: 962,
      max: 10000,
      summary: "Change the UEL to £@/week",
      type: "weekly"
    },
    child_BI: {
      title: "Child basic income",
      description: "A basic income for children is given to every child aged under 18, regardless of household income.",
      default: 0,
      value: 0,
      max: 250,
      summary: "Give a basic income of £@/week to children",
      type: "weekly"
    },
    adult_BI: {
      title: "Adult basic income",
      description: "Basic income for adults is given to individuals aged over 18 but under State Pension age.",
      default: 0,
      value: 0,
      max: 250,
      summary: "Give a basic income of £@/week to adults",
      type: "weekly"
    },
    senior_BI: {
      title: "Senior basic income",
      description: "A basic income for senior citizens is given to those over State Pension age.",
      default: 0,
      value: 0,
      max: 250,
      summary: "Give a basic income of £@/week to seniors",
      type: "weekly"
    },
  }