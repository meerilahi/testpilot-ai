
def get_presentation_score(images_dict, attempted_qns_mask):
    return {qn: 1.0 for qn in images_dict.keys() if attempted_qns_mask[qn]}