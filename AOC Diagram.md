graph TD
    %% 主流程
    Start([开始 ACO 算法]) --> InitVars[初始化参数: 蚂蚁数量, 迭代次数, alpha, beta, 蒸发率, Q值]
    InitVars --> InitPhero[初始化信息素矩阵\n initialize_pheromone_matrix]
    InitPhero --> InitVis[计算可见度矩阵\n calculate_visibility_matrix]
    
    InitVis --> IterationCheck{是否达到最大迭代次数?}
    IterationCheck -- 是 --> End([返回全局最优路径与最短距离])
    
    %% 迭代过程
    IterationCheck -- 否 --> ColonyStart[开始构建蚁群\n construct_colony]
    
    subgraph 蚁群寻优过程 (Colony Construction)
        ColonyStart --> AntInit[创建蚂蚁并随机分配起始城市\n Ant Object]
        AntInit --> CityCheck{当前蚂蚁是否已访问所有城市?}
        
        CityCheck -- 否 --> CalcProb[计算未访问城市的转移概率\n calculate_transition_probabilities]
        CalcProb --> SelectCity[轮盘赌选择下一个城市\n select_next_city]
        SelectCity --> UpdateAnt[更新蚂蚁状态: 记录城市与访问列表]
        UpdateAnt --> CityCheck
        
        CityCheck -- 是 --> CalcLength[计算该蚂蚁的总路径长度\n calculate_tour_length]
        CalcLength --> AntCheck{所有蚂蚁都完成路径了?}
        AntCheck -- 否 --> AntInit
    end
    
    %% 评估与信息素更新
    AntCheck -- 是 --> FindBest[找出本轮迭代中最优的蚂蚁\n find_best_ant]
    FindBest --> UpdateGlobal[比较并更新全局最优路径]
    UpdateGlobal --> Evaporate[信息素挥发\n evaporate_pheromone]
    Evaporate --> Deposit[基于蚂蚁路径长度释放信息素\n deposit_pheromone]
    Deposit --> IterationCheck
