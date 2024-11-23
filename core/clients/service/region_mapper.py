class RegionMapper:
    """
    State mapper for Brazilian regions.
    """
    STATE_TO_REGION = {
        'acre': 'norte',
        'alagoas': 'nordeste',
        'amapá': 'norte',
        'amazonas': 'norte',
        'bahia': 'nordeste',
        'ceará': 'nordeste',
        'distrito federal': 'centro-oeste',
        'espírito santo': 'sudeste',
        'goiás': 'centro-oeste',
        'maranhão': 'nordeste',
        'mato grosso': 'centro-oeste',
        'mato grosso do sul': 'centro-oeste',
        'minas gerais': 'sudeste',
        'paraná': 'sul',
        'paraíba': 'nordeste',
        'pará': 'norte',
        'pernambuco': 'nordeste',
        'piauí': 'nordeste',
        'rio de janeiro': 'sudeste',
        'rio grande do norte': 'nordeste',
        'rio grande do sul': 'sul',
        'rondônia': 'norte',
        'roraima': 'norte',
        'santa catarina': 'sul',
        'sergipe': 'nordeste',
        'são paulo': 'sudeste',
        'tocantins': 'norte'
    }

    @staticmethod
    def map_state_to_region(state):
        """
        Maps the provided state to its corresponding region.
        :param state: The state to map (string).
        :return: The region corresponding to the state, or "N/A" if not found.
        """
        if not state:
            return 'N/A'
        return RegionMapper.STATE_TO_REGION.get(state.strip(), 'N/A')
